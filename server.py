from twisted.web import resource
from clock_config import set_frequency

from capture_output import capture

class Home(resource.Resource):
    isLeaf = False

    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        return "<html>Hello, world!</html>"

class ClockConfig(resource.Resource):
    isLeaf = False

    def render_GET(self, request):
        if 'frequency' in request.args:
          frequency = request.args['frequency'][0] # it's a list of one item
          with capture() as out:
            result = set_frequency(frequency)
          if result:
            return "Clock set to frequency: <b>{0:s}</b>. Response below:<br/><br/>{1:s}".format(frequency, out[0].replace('\n','<br/>'))
          else:
            return "Could not set clock to frequency. Response below:<br/>{0:s}".format(out[0].replace('\n','<br/>'))
        return "No frequency provided? Add '?frequency=...' to url"

if __name__ == "__main__":
    from twisted.web import server
    from twisted.internet import reactor
    root = Home()
    root.putChild("clock", ClockConfig())
    site = server.Site(root)
    reactor.listenTCP(80, site)
    reactor.run()
