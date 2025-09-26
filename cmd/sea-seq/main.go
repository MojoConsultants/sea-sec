package main

import (
    "fmt"
    "os"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Println("SEASEQ: Please provide a spec file with spec <suite.yaml> - maiin.go:10")
        os.Exit(1)
    }
    fmt.Println("SEASEQ would run your test suite here 🚀 - maiin.go:13")
}
