# go get -u github.com/swaggo/http-swagger
# go install github.com/swaggo/http-swagger
export GOPATH=$HOME/go/
export PATH=$PATH:$GOPATH/bin/
swag init -g main.go app.go model.go
