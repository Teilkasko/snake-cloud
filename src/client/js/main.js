function rxFromIO (io, eventName) {
    return rxjs.Observable.create(observer => {
        io.on (eventName, (data) => {
            observer.next(data)
        });
        return {
            dispose : io.close
        }
    });
}

function connectionId (socket) {
	return socket.id.split('#')[1];
}

function connectAsUser (socket, username) {
	console.log("connect as user", username, connectionId(socket));
	socket.emit('command', {'command':'connect', 'username':username});
}

function initRx(canvas) {
	console.log("initRx");

    const namespace = '/snake';
    const socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    const updates = rxFromIO(socket, 'updates');
	updates.subscribe(event => {
		console.log("UPDATES", event);
	})

    const connectForm = document.getElementById("connectForm");
    const connect = rxjs.fromEvent(connectForm, 'submit');
    connect.subscribe(event => {
		const username = document.getElementById("username").value;
		connectAsUser(socket, username);
    });
}

function initArena() {
	console.log("initArena!");
	var canvas = new fabric.StaticCanvas('arena', {
		width: 400,
		height: 400
	});

	var points = [];
	var random = fabric.util.getRandomInt;

	points.push(new fabric.Point(100,100));
	points.push(new fabric.Point(200,200));
	points.push(new fabric.Point(250,150));

	console.log("POINTS", points)
	var polyLine = new fabric.Polyline(points, {
		stroke: 'black',
		opacity: 0.25,
//		stroke: new fabric.Color("rgba(1,20,100,0.5)"),
		fill: '',
		strokeWidth: 5,
		strokeLineCap: 'round',
		strokeLineJoin: 'round'
	});
	canvas.add(polyLine)

	return canvas;

}

document.addEventListener("DOMContentLoaded", function() {
	var canvas = initArena();
	initRx(canvas);
});