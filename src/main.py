def run_twee(code):
    if "print" in code:
        parts = code.split("print")[1].strip().strip('"')
        print(parts)
    elif "scream" in code:
        print("AHHHH!!!")

if __name__ == "__main__":
    # basic test
    code = 'print "hello, world" if mood is good else scream'
    run_twee(code)
