package main

import log "github.com/sirupsen/logrus"

func main() {
	log.Info("Just an INFO log, no worries")
	log.Warn("A WARN log might make us a bit nervous...")
	log.Error("Now something is really wrong!")
}
