import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define request handler class.
class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				# Send response status code
				self.send_response(200)
				# Send headers
				self.send_header('Content-Type', 'text/html')
				self.end_headers()
				
				# Send message back to client
				message = "Hello World!"
				# Write content as utf-8 data
				self.wfile.write(bytes(message, "utf8"))
				print (message)
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>&#161 Hola !</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(bytes(output, "utf8"))
				print (output)
				return

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
			output = ""
			output += "<html><body>"
			output += " <h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
			output += "</body></html>"
			self.wfile.write(bytes(output, "utf8"))
			print (output)
		except:
			pass

def main():
	try:
		# Server settings
		port = 8081
		server = HTTPServer(('', port), webserverHandler)
		print ("Web server running on port %s" % port)
		server.serve_forever()

	except KeyboardInterrupt:
		# Stop server with keyboard command 'Ctrl + C'
		print ("^C entered, stopping web server...")
		server.socket_close()

if __name__ == "__main__":
	main()