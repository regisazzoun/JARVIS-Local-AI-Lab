import React, { useState } from 'react'
import { 
  LiveKitRoom,
  useLocalParticipant,
  useTracks,
  TrackMutedIndicator,
  DisconnectButton,
  ConnectionState,
  AudioTrack
} from '@livekit/components-react'
import '@livekit/components-styles'
import './App.css'

/**
 * Composant qui affiche les informations de connexion et contrôle audio
 */
function RoomControls() {
  const localParticipant = useLocalParticipant()
  
  return (
    <div className="room-controls">
      <ConnectionState />
      
      <div className="status-bar">
        <span className="connection-status">
          {localParticipant.isConnected ? '🟢 Connecté' : '⚪ Déconnecté'}
        </span>
        <span className="identity">Identité: {localParticipant.identity || '---'}</span>
      </div>
    </div>
  )
}

/**
 * Composant qui affiche et gère les tracks audio
 */
function AudioRenderer() {
  const tracks = useTracks(['audio'], {
    onlyFor: ['local', 'remote'],
    updateOnlyExisting: false,
  })
  
  return (
    <div className="audio-section">
      <h3>🎙️ Tracks Audio Actifs</h3>
      
      <div className="track-list">
        {tracks.length === 0 ? (
          <p>Aucun track audio détecté. Assurez-vous que votre microphone est autorisé.</p>
        ) : (
          tracks.map((pub) => (
            <div key={pub.sid} className="track-item">
              <div className="track-info">
                <strong>{pub.participant.name || pub.participant.identity}</strong>
                {pub.source === 'microphone' && <span className="source-badge">Micro</span>}
                {pub.source === 'audio' && <span className="source-badge">Audio</span>}
              </div>
              <div className="track-controls">
                <TrackMutedIndicator trackPublication={pub} />
                {!pub.isLocal && (
                  <AudioTrack trackPublication={pub} autoPlay={true} />
                )}
                {pub.isLocal ? (
                  <span className="local-badge">Local</span>
                ) : (
                  <span className="remote-badge">Remote</span>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

/**
 * Composant principal de la salle de conversation
 */
function ConversationRoom() {
  return (
    <div className="conversation-room">
      <div className="room-header">
        <h2>🎙️ Conversation JARVIS - LiveKit</h2>
        <RoomControls />
      </div>
      
      <div className="room-content">
        <AudioRenderer />
        
        <div className="instructions">
          <h3>Instructions:</h3>
          <ul>
            <li>Parlez dans votre microphone</li>
            <li>JARVIS détectera votre voix et répondra</li>
            <li>Vous pouvez l'interrompre pendant qu'il parle</li>
            <li>La transcription est disponible dans les logs de l'agent</li>
          </ul>
        </div>
        
        <div className="room-actions">
          <DisconnectButton className="btn-disconnect" />
        </div>
      </div>
    </div>
  )
}

/**
 * Composant principal de l'application
 */
function App() {
  const [connected, setConnected] = useState(false)
  const [serverUrl, setServerUrl] = useState('ws://localhost:7880')
  const [roomName, setRoomName] = useState('jarvis-room')
  
  const handleConnect = () => {
    setConnected(true)
  }
  
  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 JARVIS - Prototype Vocale LiveKit</h1>
        <p>Mission 23 : Interface de conversation temps réel</p>
      </header>
      
      {!connected ? (
        <div className="connect-section">
          <div className="info-card">
            <h2>Bienvenue sur le prototype vocal JARVIS</h2>
            <p>Ce client Web permet de tester l'interface vocale temps réel avec LiveKit.</p>
            <ul className="features-list">
              <li>✅ Reconnaissance vocale en français (Whisper)</li>
              <li>✅ Synthèse vocale naturelle (Piper)</li>
              <li>✅ Modèle IA local (Ollama sur Dell)</li>
              <li>✅ Interruption de parole possible</li>
              <li>✅ Transcription en temps réel</li>
            </ul>
          </div>
          
          <div className="connection-form">
            <h3>Connexion au serveur</h3>
            <div className="form-group">
              <label htmlFor="server-url">URL Serveur LiveKit:</label>
              <input 
                type="text" 
                id="server-url"
                value={serverUrl}
                onChange={(e) => setServerUrl(e.target.value)}
                placeholder="ws://localhost:7880"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="room-name">Nom de la salle:</label>
              <input 
                type="text" 
                id="room-name"
                value={roomName}
                onChange={(e) => setRoomName(e.target.value)}
                placeholder="jarvis-room"
              />
            </div>
            
            <button onClick={handleConnect} className="btn-connect">
              🎙️ Démarrer la conversation
            </button>
            
            <div className="connection-info">
              <strong>Note importante:</strong> Assurez-vous que:
              <ul>
                <li>LiveKit Server est en cours d'exécution (port 7880)</li>
                <li>L'agent Python LiveKit est démarré</li>
                <li>Votre navigateur autorise l'accès au microphone</li>
              </ul>
            </div>
          </div>
        </div>
      ) : (
        <LiveKitRoom
          serverUrl={serverUrl}
          roomName={roomName}
          connect={true}
          video={false}
          audio={true}
          onDisconnected={() => setConnected(false)}
        >
          <ConversationRoom />
        </LiveKitRoom>
      )}
      
      <footer className="app-footer">
        <p>JARVIS Local AI Lab - Mission 23 - Développé par JARVIS autonome</p>
        <p><small>Horloge: 2026-10-19T18:27:57+02:00</small></p>
      </footer>
    </div>
  )
}

export default App
