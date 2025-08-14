# Fast API playground async and single worker

Getting started

Have uv installed 

    uv venv --python=3.12 .venv
    
    source ./.venv/bin/activate

    uv pip install -r requirements.txt

Have go 1.24.4 installed 

    install the load runner 

    go install github.com/tsliwowicz/go-wrk@latest

Two Demos:

    Both are regarding async and sync
    
---

    1: A single service that has two endpoints 
        * blocking
        or
        * None blocking

    From root run 
        ./start.sh service
        This calls the sync (blocking) endpoint
        go-wrk -c 10 -d 5  -T  3000 http://localhost:9000/blocking-io

        this calls the async (none blocking) endpoint
        go-wrk -c 10 -d 5  -T  3000 http://localhost:9000/non-blocking-io

        this calls the async (none blocking) endpoint
        go-wrk -c 10 -d 5  -T  3000 http://localhost:9000/non-blocking-io-method

---

    2: Interservice communication via a server that has blockig endpoint calling 
        * Blocking (sync) service endpoint
        or
        * None blocking (async) service endpoint
    
    from root open three terminals and run 

    Terminal 1
    ./start.sh service

    Terminal 2
    ./start.sh main

    Terminal 3 

    This calls the blocking endpoint (sync) which calls a blocking service endpoint (async)
    go-wrk -c 10 -d 5  -T  3000  http://localhost:8000?call_type=blocking

    This calls the blocking endpoint (sync) which calls a non blocking service endpoint (async)
    go-wrk -c 10 -d 5  -T  3000  http://localhost:8000?call_type=non_blocking_thread

    This calls the blocking endpoint (sync) which calls a non blocking service endpoint (async)
    go-wrk -c 10 -d 5  -T  3000  http://localhost:8000?call_type=non_blocking_method

