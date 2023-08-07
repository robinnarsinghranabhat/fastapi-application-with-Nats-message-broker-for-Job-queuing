
### Python producer-consumer with NATS messaging Demo
Assume one of your endpoint needs to do some cpu-heavy file processing. 
Using nats messaging, the endpoint publishes url of file as message which can be consumed by 
one of the competing consumer.


### Setup :
1. Install and run the NATS server. If you have docker, just do : 
- `docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name nats-server  -ti nats:latest -js`
Otherwise, check the nats documentation.

2. Run the publisher endpoint. Anytime we get a request endpoint, an message is pushed to nats-server 
- `uvicorn publisher_app:app --host 0.0.0.0 --port 8001`

3. Run this command in multiple terminals to load multiple consumers.
- `python service.py`

### USAGE : 
- GOTO : `http://localhost:8001/docs` and try out the '/process_file/file_name' endpoint. You should see messages distributed almost equally to both file-processing consumers/services.

### NOTES : 
- It's never a good idea to send large files as messages. Only send the pointer to file like s3-url. 