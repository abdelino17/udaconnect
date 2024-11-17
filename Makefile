list:
	grpcurl --plaintext localhost:5000 list
	grpcurl --plaintext localhost:5000 list LocationService

message:
	grpcurl --plaintext localhost:5000 describe .LocationMessage

call:
	grpcurl --plaintext -d @ localhost:30002 LocationService.Create < grpc_test.json
