   <script>
    let isRecording = false;
    let mediaRecorder = null;
    let audioChunks = [];

    // Typing Indicator Element
    let typingIndicator = null;

    function addMessage(message, isUser) {
        const messageDiv = $('<div>')
            .addClass('message')
            .addClass(isUser ? 'user-message' : 'bot-message')
            .text(message);

        // Set the avatar images dynamically
        const avatarDiv = $('<div>').addClass('avatar');
        if (isUser) {
            avatarDiv.css('background-image', 'url("/static/img/guy.jpg")'); // Replace with your user avatar URL
        } else {
            avatarDiv.css('background-image', 'url("/static/img/bot.jpg")'); // Replace with your bot avatar URL
        }
        messageDiv.prepend(avatarDiv);

        $('#chatContainer').append(messageDiv);
        $('#chatContainer').scrollTop($('#chatContainer')[0].scrollHeight);
    }

    function playAudio(base64Audio) {
        const audio = new Audio('data:audio/wav;base64,' + base64Audio);
        audio.play();
    }

    function showTypingIndicator() {
        // Prevent multiple indicators
        if (typingIndicator) return;

        typingIndicator = $('<div>')
            .addClass('message bot-message typing-indicator')
            .html(`
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            `);
        $('#chatContainer').append(typingIndicator);
        $('#chatContainer').scrollTop($('#chatContainer')[0].scrollHeight);
    }

    function hideTypingIndicator() {
        if (typingIndicator) {
            typingIndicator.remove();
            typingIndicator = null;
        }
    }

    $('#sendText').click(function() {
        const message = $('#userInput').val().trim();
        if (!message) return;

        addMessage(message, true);
        $('#userInput').val('');

        // Show typing indicator
        showTypingIndicator();

        $.ajax({
            url: '/process_text',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: message }),
            success: function(response) {
                console.log('Text Response:', response); // Debug: Log server response
                hideTypingIndicator();
                addMessage(response.response, false);
                if (response.audio) {
                    playAudio(response.audio);
                }
            },
            error: function(xhr, status, error) {
                console.error('Text Error:', error); // Debug: Log text errors
                hideTypingIndicator();
                addMessage('Error: ' + error, false);
            }
        });
    });

    $('#userInput').keypress(function(e) {
        if (e.which == 13) {
            $('#sendText').click();
        }
    });

    function convertToWav(blob) {
        return new Promise(async (resolve) => {
            const audioContext = new AudioContext();
            const arrayBuffer = await blob.arrayBuffer();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            const offlineContext = new OfflineAudioContext(1, audioBuffer.duration * 16000, 16000);
            const source = offlineContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(offlineContext.destination);
            source.start();
            const resampledBuffer = await offlineContext.startRendering();
            const samples = resampledBuffer.getChannelData(0);
            const wavBuffer = new ArrayBuffer(44 + samples.length * 2);
            const view = new DataView(wavBuffer);
            const writeString = (offset, str) => {
                for (let i = 0; i < str.length; i++) {
                    view.setUint8(offset + i, str.charCodeAt(i));
                }
            };
            writeString(0, 'RIFF');
            view.setUint32(4, 36 + samples.length * 2, true);
            writeString(8, 'WAVE');
            writeString(12, 'fmt ');
            view.setUint32(16, 16, true);
            view.setUint16(20, 1, true);
            view.setUint16(22, 1, true);
            view.setUint32(24, 16000, true);
            view.setUint32(28, 16000 * 2, true);
            view.setUint16(32, 2, true);
            view.setUint16(34, 16, true);
            writeString(36, 'data');
            view.setUint32(40, samples.length * 2, true);
            let offset = 44;
            for (let i = 0; i < samples.length; i++, offset += 2) {
                const s = Math.max(-1, Math.min(1, samples[i]));
                view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
            }
            resolve(new Blob([wavBuffer], { type: 'audio/wav' }));
        });
    }

    $('#startRecording').click(async function () {
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const wavBlob = await convertToWav(audioBlob);
                    const formData = new FormData();
                    formData.append('audio', wavBlob);

                    // Show typing indicator
                    showTypingIndicator();

                    try {
                        const response = await fetch('/process_voice', { method: 'POST', body: formData });
                        const data = await response.json();
                        hideTypingIndicator();
                        if (data.transcript) {
                            addMessage(data.transcript, true);
                        }
                        if (data.response) {
                            addMessage(data.response, false);
                        }
                        if (data.audio) {
                            playAudio(data.audio);
                        }
                    } catch (error) {
                        hideTypingIndicator();
                        addMessage('Error: ' + error.message, false);
                    }

                    $('#recordingStatus').hide();
                    $('#startRecording').removeClass('recording').text('Start Voice');
                    $('#stopRecording').prop('disabled', true);
                    $('#startRecording').prop('disabled', false);
                };

                mediaRecorder.start();
                isRecording = true;
                $('#startRecording').addClass('recording').text('Recording...');
                $('#recordingStatus').show();
                $('#stopRecording').prop('disabled', false);
                $('#startRecording').prop('disabled', true);

            } catch (error) {
                addMessage('Error: ' + error.message, false);
            }
        }
    });

    $('#stopRecording').click(function () {
        if (isRecording && mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            isRecording = false;
            $('#recordingStatus').hide();
            $('#startRecording').removeClass('recording').text('Start Voice');
            $('#stopRecording').prop('disabled', true);
            $('#startRecording').prop('disabled', false);
        }
    });

</script>