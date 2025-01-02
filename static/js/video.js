console.log("video.js has been loaded successfully!");

// Dynamically load YouTube IFrame Player API
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;

// YouTube IFrame API Ready Callback
function onYouTubeIframeAPIReady() {
    console.log("YouTube API is ready.");
    player = new YT.Player('player', {
        height: '100%',
        width: '100%',
        videoId: '-BJF4BmbsZ8', // Replace with your video ID
        playerVars: {
            autoplay: 1,           // Start video automatically
            controls: 0,           // Hide controls
            mute: 1,               // Mute video
            modestbranding: 1,     // Minimal YouTube branding
            rel: 0,                // No unrelated videos at the end
        },
        events: {
            onStateChange: onPlayerStateChange, // Event handler for state changes
            onReady: (event) => {
                console.log("Video player is ready.");
                event.target.seekTo(12); // Start video at 12 seconds
                event.target.playVideo(); // Ensure the video starts playing
            }
        }
    });
}

// State Change Handler
function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.PLAYING) {
        monitorPlayback(); // Monitor playback time when the video starts playing
    }
}

// Monitor Playback Time
function monitorPlayback() {
    setInterval(() => {
        if (player && player.getCurrentTime) {
            const currentTime = player.getCurrentTime();

            if (currentTime >= 60) {
                console.log("Reached 60 seconds. Restarting at 9 seconds...");
                player.seekTo(9); // Restart at 9 seconds
            }
        }
    }, 500); // Check every 500ms for precise control
}
