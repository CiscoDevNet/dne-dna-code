# NeXt UI Framework

NeXt UI toolkit is an HTML5/JavaScript based toolkit for network web application. It provides a network centric topology UI component featuring high performance and rich functionality. NeXt can display large complex network topologies, aggregated network nodes, traffic/path/tunnel/group visualizations and it includes different layout algorithms, map overlays, and preset user friendly interactions. NeXt can work together with DLUX to build ODL apps.

Homepage : https://wiki.opendaylight.org/view/NeXt:Main

UI Toolkit Quicklook : https://www.youtube.com/watch?v=gBsUDu8aucs

Current version : 1.0.0

## Key Features

* Large complex network topologies
* Aggregated network nodes
* Traffic/path/tunnel/group visualizations
* Different layout algorithms
* Map overlays
* Preset user-friendly interactions

## File structure
```
next/
  |- css/
  |  |- next.css // next stylesheet file
  |  |- next.min.css // minimized stylesheet file
  |  |- next-componentized.css
  |  |- next-componentized.min.css
  |- js
  |  |- next.js // next js library
  |  |- next.min.js // minimized js library
  |- fonts/ // font resources foler
  |  doc/ //APi manual
  |- README.md
```

## Quick start

1) Create a HTML file.

```HTML
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="css/next.css">
        <script src="js/next.js"></script>
    </head>
    <body>
    <script type="text/javascript">
    //next code
    </script>
    </body>
</html>
```

2) Edit next code

```javascript
// Initialize a topology component
var topo = new nx.graphic.Topology({
});

// Create new app
var app = new nx.ui.Application();

// Attach topo to app
topo.attach(app);
```

3) Open html file with Chrome

### Tutorials and Sample code

Tutorials : https://wiki.opendaylight.org/view/NeXt:Main

Opendaylight sample code intergrate DLUX with NeXt: https://github.com/CiscoDevNet/opendaylight-sample-apps

BIERMAN : https://github.com/zverevalexei/bierman-gui

## Build instructions from source code

Git :  https://git.opendaylight.org/gerrit/p/next

### Environment requirements

In order to build NeXt from sources, you must have [Node.js](https://nodejs.org/) installed. 

After that, make sure to have [Grunt](https://www.npmjs.com/package/grunt) installed. To do so, run:

```
npm install grunt
```

### Build process
* ```npm install``` to install npm modules
* ```grunt``` to build from sources

### Authorized Devs Only: Bower Updates
You should only update Bower if the build is stable, or a major issue has been fixed.

To do so, type in the command line:

```
node update-bower.js -u {{GITHUB USERNAME}} -p {{GITHUB PASSWORD}} -v {{VERSION NUMBER}}
```
Make sure to turn ```{{GITHUB USERNAME}}```, ```{{GITHUB PASSWORD}}``` and ```{{NEW VERSION}}``` into appropriate values.

Example: 

```
node update-bower.js -u gituser -p 123456 -v 0.1.0
```

Leave the terminal window open until you see ```Done!``` message.

## Who's Using NeXt
Here we feature a few customers who choose NeXt framework as their topology visualization tool and use it in their products.

* [Cisco](https://cisco.com/)
* [Verizon](https://www.verizonwireless.com)
* [AT&T](https://att.com)
* [HP Enterprise](https://hpe.com)
* [NTS Netzwerk Telekom Service AG](http://www.nts.eu/en/)

Are you *next*?

## Bugs

[Open Bugs](https://bugs.opendaylight.org/buglist.cgi?bug_status=__open__&product=next)

## Team

* Aikepaer Abuduweili (aaikepae@cisco.com)
* Kang Li (lkang2@cisco.com)
* Alexei Zverev (alzverev@cisco.com)
* Xu Yangyang(yangyxu@cisco.com)
