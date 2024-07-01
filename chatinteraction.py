def request(reqtxt):
    import cohere
    co = cohere.Client(api_key="TEBEYk3DFOByqpPUq26aOE8kuXIvEVouui9gIuZ6")
    
    
    response = co.chat(
        model="command-r-plus",
        message=reqtxt
    )
    
    print(response.text)
    return response.text
