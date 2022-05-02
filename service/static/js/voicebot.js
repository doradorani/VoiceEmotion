document.addEventListener('DOMContentLoaded', () => {

	window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

	let p = document.createElement('p');
	const paper = document.querySelector('.paper');
	paper.appendChild(p);

	const recognition = new SpeechRecognition();
	recognition.interimResults = true;
	recognition.addEventListener('result', e => {
		console.log(e.results);
		const transcript = Array.from(e.results)
			.map(results => results[0])
      
			.map(result => result.transcript)
			.join('')
		let script = transcript
			.replace(/\b(smile|smiling|(ha)+)\b/gi, '😃')
			.replace(/\b(happy|celebrate)\b/gi, '🎉')
			.replace(/\b(angry|serious)\b/gi, '😠')
			.replace(/\bclap\b/gi, '👏')
			.replace(/\b(okay|ok|okie)\b/gi, '👍')
			.replace(/\b(eat|eating|hungry)\b/gi, '🍔')
			.replace(/\bcry\b/gi, '😥');
		const regex = /open\s?(facebook|google|twitter|youtube|github)/i;
		if(regex.test(script)){
			console.log(script.match(regex)[1]);
			const link = openWebsite(script.match(regex)[1]);
			script = script.replace(regex,link);
		}
		p.innerHTML = script;
		p.scrollIntoView(true);
		if (e.results[0].isFinal) {
			p = document.createElement('p');
			paper.appendChild(p);
		}
	});
	recognition.addEventListener('end', () => {
		if (document.getElementById('toggle').checked) {
			recognition.start();
		} else {
			recognition.stop();
		}
	});
	const toggle = document.getElementById('toggle');
	toggle.addEventListener('change', e => {
		if (e.target.checked) {
			recognition.start();
		} else {
			recognition.abort();
			console.log('stopped');
		}
	});
	const clear = document.getElementById('clear');
	clear.addEventListener('click', e => {
		e.preventDefault();
		paper.innerHTML = '';
		p = document.createElement('p');
		paper.appendChild(p);
	});
});

function getWeather() {
	
}

function openWebsite(name) {
	console.log(`inside func: ${name}`);
	const validSites = ['facebook', 'google', 'twitter', 'youtube', 'github'];
	if(validSites.includes(name.toLowerCase())) {
		window.open(`http://${name}.com`, '_blank');
		return `<a href='http://${name}.com' target='_blank'>Open ${name}</a>`
	}
}

