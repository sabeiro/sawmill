// Database handler for storage.lightmerer.io
//
// This documentation describes example APIs 
//
//     Schemes: https
//     BasePath: /
//     Version: 1.0.0
//     License: CC by-nc-sa https://creativecommons.org/licenses/by-nc-sa/4.0/
//     Contact: Giovanni Marelli https:// intertino.it 
//     Host: sabeiro/
//
//     Consumes:
//     - application/json
//
//     Produces:
//     - application/json
//
//     Security:
//     - bearer
//
//     SecurityDefinitions:
//     bearer:
//          type: apiKey
//          name: Authorization
//          in: header
//
package main

import (
  "os"
)
// @title Go ingest app
// @version 1.0
// @description Handler for selected db operations, example: https://gitlab.com/lightmeter/data-pipeline/-/blob/main/parse_source/test_goBackend.py
// @termsOfService http://swagger.io/terms/
// @contact.name API Support
// @contact.email via@l
// @license.name CC by-nc-sa
// @license.url https://creativecommons.org/licenses/by-nc-sa/4.0/
// @BasePath /
func main() {
  a := App{}
  a.Initialize(
    os.Getenv("DB_HOST"),
    os.Getenv("DB_USER_GO"),
    os.Getenv("DB_PASS_GO"),
    os.Getenv("DB_NAME"),
  )
	// router := mux.NewRouter().StrictSlash(true)
  a.Run(":5006")
}

