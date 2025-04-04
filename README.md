# Lora

![image](https://github.com/user-attachments/assets/c0455180-2eff-4fac-96ff-28ca391b72ab)

A simple Lua to Python cross-compiler.
# Lua to Python Tokenizer
Tokenizer for Lua source code written in Python as part of CMPSC 470


# Lua to Python Tokenizer

A Python-based tokenizer for Lua source code, developed as part of CMPSC 470 (Spring 2025) at Penn State. The tokenizer processes Lua files and outputs a structured report of tokens including literals, operators, variables, reserved words, and more.

## 🧠 Authors
- Tommy Lu
- Ishraq Syed
- Richard Wong

## 📚 Course
CMPSC 470, Section 001 – Spring 2025

## 🧩 Project Overview

The tokenizer scans Lua code and categorizes each token using regular expressions and lexical analysis via `lexer.py`. The tool skips over comments, handles Lua syntax features, and produces a JSON-formatted report.

### ✅ Features
- Handles literals: numbers, strings, booleans, nil
- Detects arithmetic, logical, and relational operators
- Recognizes Lua reserved keywords
- Counts unique and duplicate variables
- Skips single-line and multi-line comments
- Supports integration with `lexer.py`

## 🗂️ File Structure

