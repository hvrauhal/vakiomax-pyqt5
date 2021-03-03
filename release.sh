#!/usr/bin/env zsh
fbs freeze
fbs installer
mv target/VakioMax4.dmg target/VakioMax4-$(git rev-parse --short HEAD).dmg
