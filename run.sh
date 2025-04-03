#!/bin/bash

rm -rf reports/*
rm -rf logs/*

pytest tests/

open reports/report.html
