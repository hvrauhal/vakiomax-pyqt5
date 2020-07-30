#!/usr/bin/env bash 
convert logo.png -resize 1024x1024 ./mac/1024.png
convert logo.png -resize 128x128 ./mac/128.png
convert logo.png -resize 512x512 ./mac/512.png
convert logo.png -resize 256x256 ./mac/256.png
convert logo.png -resize 1024x1024 ./linux/1024.png
convert logo.png -resize 128x128 ./linux/128.png
convert logo.png -resize 512x512 ./linux/512.png
convert logo.png -resize 256x256 ./linux/256.png
convert logo.png -resize 48x48 ./base/48.png
convert logo.png -resize 64x64 ./base/64.png
convert logo.png -resize 16x16 ./base/16.png
convert logo.png -resize 32x32 ./base/32.png
convert logo.png -resize 24x24 ./base/24.png
