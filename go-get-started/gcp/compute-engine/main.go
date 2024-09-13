package main

import (
    "fmt"
    "log"
    "net/http"
    "os"
)

func main() {
    lfEnv := os.Getenv("LAUNCHFLOW_ENVIRONMENT")
    if lfEnv == "" {
        log.Fatal("LaunchFlow environment not set")
    }
    port := os.Getenv("PORT")
    if port == "" {
        port = "3000"
    }
    host := os.Getenv("HOST")
    if host == "" {
        host = "127.0.0.1"
    }
    address := fmt.Sprintf("%s:%s", host, port)

    greeting := fmt.Sprintf("Hello from %s!", lfEnv)
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, greeting)
    })

    log.Printf("Server listening on %s", address)
    log.Fatal(http.ListenAndServe(address, nil))
}
