package main

import (
    "fmt"
    "os"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Println("SEA-SEQ: Please provide a spec file with --spec <suite.yaml>")
        os.Exit(1)
    }
    fmt.Println("SEA-SEQ would run your test suite here 🚀")
}
