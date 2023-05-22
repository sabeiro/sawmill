package main
import (
	"fmt"
	"net/http"
	"encoding/base64"
	"strings"
	"time"
	"github.com/dgrijalva/jwt-go"
)
//  ---------------------------------Auth---------------------------------- 
func userpassword() (userPasswordMap map[string]string) {
	userPasswordMap = make(map[string]string)
	userPasswordMap["user_scrap"] = "wga53tqitd#@"
	userPasswordMap["user_prod"]  = "T#QgAQGGRsag325"
	userPasswordMap["user_batch"] = "AREWR%Y#2352qaAd"
	return
}
func generateJWT() (tokenString string, err error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"iat": time.Now().Unix(),
		"exp": time.Now().Add(time.Hour * 1).Unix()})
	tokenString, err = token.SignedString([]byte("secret"))
	return tokenString, err
}
func authenticateRequest(authHeader string) bool {
	data, err := base64.StdEncoding.DecodeString(authHeader)
	if err != nil {
		fmt.Println("error:", err)
		return false
	}
	userpwd := strings.Split(string(data), ":")
	userpwdmap := userpassword()
	if userpwdmap[userpwd[0]] == userpwd[1] {
		return true
	}
	return false
}
 func authenticateJWT(header http.Header) bool {
	jwtString := header.Get("Authentication")
	if len(jwtString) == 0 {
		return false
	}
	token, err := jwt.Parse(jwtString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}
		return []byte("secret"), nil
	})
	if err == nil && token.Valid {
		return true
	} else {
		return false
	}
	return false
}
