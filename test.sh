#!/bin/bash

py.test --cov breaker --cov-report term-missing --cov-config coverage.ini
