const socket = new WebSocket('ws://relay');

socket.onopen = function(event) {
    socket.send('["REQ", "133742069", {"kinds": [1]}]');
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data[0] === "EVENT") {
        if(data[2].kind === 1) {
            const id = data[2].id;
            const content = data[2].content;
            const pubkey = data[2].pubkey;
            const pubkeyShortened = `${pubkey.slice(0, 3)}...${pubkey.slice(-3)}`;
            const createdAt = data[2].created_at;
            const date = new Date(createdAt * 1000);
            const formattedTime = date.toLocaleString();
            var divCol = document.createElement('div');
            divCol.setAttribute('class', 'col');
            var divCard = document.createElement('div');
            divCard.setAttribute('class', 'card shadow-sm');
            var divCardBody = document.createElement('div');
            divCardBody.setAttribute('class', 'card-body');
            var pCardText = document.createElement('p');
            pCardText.setAttribute('class', 'card-text');
            pCardText.innerHTML = content;
            var divBtnFlex = document.createElement('div');
            divBtnFlex.setAttribute('class', 'd-flex justify-content-between align-items-center');
            var divBtnGroup = document.createElement('div');
            divBtnGroup.setAttribute('class', 'btn-group');
            var smallText = document.createElement('small');
            smallText.setAttribute('class', 'text-body-secondary');
            smallText.innerHTML = formattedTime;

            var smallTextId = document.createElement('small');
            smallTextId.setAttribute('class', 'text-body-secondary');
            smallTextId.innerHTML = id;

            divBtnFlex.appendChild(divBtnGroup);
            divBtnFlex.appendChild(smallText);
            divCardBody.appendChild(pCardText);
            divCardBody.appendChild(divBtnFlex);
            divCardBody.appendChild(smallTextId);

            divCard.appendChild(divCardBody);
            divCol.appendChild(divCard);
            document.getElementById('notes-row').appendChild(divCol);
        }
    }
};