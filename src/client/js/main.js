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

function initRx() {
	console.log("initRx");

    const namespace = '/snake';
    const socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    const updates = rxFromIO(socket, 'updates');
    updates.pipe(
    	rxjs.operators.tap(event => console.log("UPDATES", event))
    );

    const connectForm = document.getElementById("connectForm");
    const connect = rxjs.fromEvent(connectForm, 'submit');
    connect.subscribe(event => {
		const username = document.getElementById("username").value;
		connectAsUser(socket, username);
    });
}

document.addEventListener("DOMContentLoaded", function() {
	initRx();
});