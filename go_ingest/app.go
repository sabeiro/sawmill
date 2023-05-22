package main
import (
  "database/sql"
  "fmt"
  "os"
  _ "io"
  _ "strings"
  "log"
  "net/http"
	"github.com/gorilla/mux"
  "strconv"
  "encoding/json"
  _ "github.com/lib/pq"
	httpSwagger "github.com/swaggo/http-swagger"
  //  _ "github.com/swaggo/http-swagger/example/gorilla/docs"
	//  _ "docs"
  // "intertino/go_ingest/docs"
)
type App struct {
  Router  *mux.Router
  DB      *sql.DB
}
//  ---------------------------------------------Db-----------------------------------------
func (a *App) Initialize(host, user, password, dbname string) {
    connectionString := fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=disable", host, user, password, dbname)
    fmt.Printf("host=%s dbname=%s", host, dbname) 
    var err error
    a.DB, err = sql.Open("postgres", connectionString)
    if err != nil {
      log.Fatal(err)
    }
    a.Router = mux.NewRouter()
    a.initializeRoutes()
}
// Select from table
// @Summary select from table
// @Description chose table and fields to extract, example: {"id":0,"action":"*","table":"db.product","filter":"WHERE id=1"}
// @Tags sql
// @Accept  json
// @Produce  json
// @Param query body queryD true "add entry to table"
// @Success 200 
// @Router /select [post]
func (a *App) getEntry(w http.ResponseWriter, r *http.Request) {
  	if !authenticateJWT(r.Header) {
	  	w.WriteHeader(http.StatusUnauthorized)
		  return
	  } 
    var p queryD
    decoder := json.NewDecoder(r.Body)
    if err := decoder.Decode(&p); err != nil {
        fmt.Printf("error: %s\n",err.Error())
        respondWithError(w, http.StatusBadRequest, "Invalid request payload")
        return
    }
    list, err := p.getEntry(a.DB);
    if err != nil {
        switch err {
        case sql.ErrNoRows:
            respondWithError(w, http.StatusNotFound, "Entry not found")
        default:
            respondWithError(w, http.StatusInternalServerError, err.Error())
        }
        return
    }
    respondWithJSON(w, http.StatusOK, list )
}
// Insert into table
// @Summary insert into table
// @Description insert into table, example: {"id":0,"action":"(name,price) values ('test_prod',11.2)","table":"db.product","filter":""}
// @Tags sql 
// @Accept  json
// @Produce  json
// @Param query body queryD true "add entry to table"
// @Success 200 
// @Router /create [post]
func (a *App) createEntry(w http.ResponseWriter, r *http.Request) {
  	if !authenticateJWT(r.Header) {
	  	w.WriteHeader(http.StatusUnauthorized)
		  return
	  } 
    var p queryD
    decoder := json.NewDecoder(r.Body)
    if err := decoder.Decode(&p); err != nil {
        fmt.Printf("error: %s\n",err.Error())
        respondWithError(w, http.StatusBadRequest, "Invalid request payload")
        return
    }
    defer r.Body.Close()
    if err := p.createEntry(a.DB); err != nil {
        fmt.Println(err.Error() ) 
        respondWithError(w, http.StatusInternalServerError, err.Error())
        return
    }
    respondWithJSON(w, http.StatusCreated, p)
}
// Update entry
// @Summary update entry
// @Description update entry, example: /update/product/1
// @Tags sql
// @Accept  json
// @Produce  json
// @Param query body queryD true "add entry to table"
// @Success 200 
// @Router /update/{table}/{id} [get]  
func (a *App) updateEntry(w http.ResponseWriter, r *http.Request) {
  	if !authenticateJWT(r.Header) {
	  	w.WriteHeader(http.StatusUnauthorized)
		  return
	  } 
    vars := mux.Vars(r)
    id, err := strconv.Atoi(vars["id"])
    if err != nil {
        respondWithError(w, http.StatusBadRequest, "Invalid product ID")
        return
    }
    var p queryD
    decoder := json.NewDecoder(r.Body)
    if err := decoder.Decode(&p); err != nil {
        respondWithError(w, http.StatusBadRequest, "Invalid resquest payload")
        return
    }
    defer r.Body.Close()
    p.ID = id
    if err := p.updateEntry(a.DB); err != nil {
        respondWithError(w, http.StatusInternalServerError, err.Error())
        return
    }
    respondWithJSON(w, http.StatusOK, p)
}
// Delete entry
// @Summary delete entry
// @Description delete entry, example: /delete/products/1
// @Tags sql 
// @Accept  json
// @Produce  json
// @Param query body queryD true "add entry to table"
// @Success 200 
// @Router  /delete/{table}/{id} [get]  
func (a *App) deleteEntry(w http.ResponseWriter, r *http.Request) {
  	if !authenticateJWT(r.Header) {
	  	w.WriteHeader(http.StatusUnauthorized)
		  return
	  } 
    vars := mux.Vars(r)
    p := queryD{Filter: "where id = " + vars["id"], Table: vars["table"] }
    if err := p.deleteEntry(a.DB); err != nil {
        fmt.Println(err.Error() ) 
        respondWithError(w, http.StatusInternalServerError, err.Error())
        return
    }
    respondWithJSON(w, http.StatusOK, map[string]string{"result": "success"})
}
func respondWithError(w http.ResponseWriter, code int, message string) {
    respondWithJSON(w, code, map[string]string{"error": message})
}
func respondWithJSON(w http.ResponseWriter, code int, payload interface{}) {
    response, _ := json.Marshal(payload)
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(code)
    w.Write(response)
}
//  -----------------------------routes-------------------------------------
func (a *App) Run(addr string) {
  log.Fatal(http.ListenAndServe(":5006", a.Router))
}
// Authenticate
// @Summary get access token
// @Description Access token for db queries, send an header base64(user:pass), ex: "Authentification": "XNlcl9zY3J". Use the obtained token in future requests as: headers["Authentication"] = token
// @Tags auth
// @Accept  json
// @Produce  json
// @Success 200 
// @Router /authenticate [get]
func (a *App) authenticateHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	authHeader := r.Header.Get("Authentication")
	if len(authHeader) == 0 || !authenticateRequest(authHeader) {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}
	token, err := generateJWT()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
	}
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(token); err != nil {
		panic(err)
	}
}
// Add platform token
// @Summary add platform token to header
// @Description add platform token to header
// @Tags auth
// @Accept  json
// @Produce  json
// @Success 200 
// @Router /route-request [get]
func (a *App) routeRequest(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/x-www-form-urlencoded")
	w.Header().Set("X-Api-Key", os.Getenv("MAILREACH_TOKEN"))
	authHeader := r.Header.Get("Authentication")
	if len(authHeader) == 0 || !authenticateRequest(authHeader) {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}
	token, err := generateJWT()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
	}
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(token); err != nil {
		panic(err)
	}
}
func getPage(pageNum int) interface{} {
	pages := []string{"This is page 1",
		"This is page 2",
		"This is page 3"}
	if pageNum > len(pages) {
		log.Print("Invalid PageNum")
    errorCode := `{"status": "error","message": "page number doesn't exist"}`
    return errorCode
	}
	return pages[pageNum]
}
func (a *App) getPageHandler(w http.ResponseWriter, r *http.Request) {
	if !authenticateJWT(r.Header) {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}
	vars := mux.Vars(r)
	pageNum, _ := strconv.Atoi(vars["pageNum"])
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Access-Control-Allow-Origin", "*")
	fmt.Println(getPage(pageNum))
	if err := json.NewEncoder(w).Encode(getPage(pageNum)); err != nil {
		panic(err)
	}
}
func (a *App) indexPage(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w,"Hello, Giossip.")
}
func (a *App) initializeRoutes() {
    a.Router.HandleFunc("/", a.indexPage).Methods("GET")
    a.Router.HandleFunc("/book/page/{pageNum:[0-9][0-9]*}", a.getPageHandler).Methods("GET")
    a.Router.HandleFunc("/authenticate", a.authenticateHandler).Methods("GET")
    a.Router.HandleFunc("/create", a.createEntry).Methods("POST")
    a.Router.HandleFunc("/select", a.getEntry).Methods("POST")
    a.Router.HandleFunc("/route-request", a.routeRequest).Methods("POST")
    a.Router.HandleFunc("/update/{table}/{id:[0-9]+}", a.updateEntry).Methods("PUT")
    a.Router.HandleFunc("/delete/{table}/{id:[0-9]+}", a.deleteEntry).Methods("DELETE")
    a.Router.PathPrefix("/apidocs/").Handler(httpSwagger.Handler(
  	  // httpSwagger.URL("http://localhost:5006/static/swagger.json"), 
  	  httpSwagger.URL("https://ingest.storage.lightmeter.io/static/swagger.json"), 
	  	  //  httpSwagger.DeepLinking(true),
		    httpSwagger.DocExpansion("none"),
  		  //  httpSwagger.DomID("#swagger-ui"),
	    )).Methods(http.MethodGet)
    a.Router.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("./docs/"))))
  	// registerV1Routes(a.Router)
}
// func registerV1Routes(r *mux.Router) {
// 	v1 := r.PathPrefix("/v1").Subrouter()
// 	api.RegisterRepoRoutes(v1, "/repo")
// 	api.RegisterUserRoutes(v1, "/user")
// }
