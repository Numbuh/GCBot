#include "ScriptReader.hpp"

#include <cstring>

ScriptReader::ScriptReader(const uint8_t *pData)
    : m_commands(nullptr), m_commandCount(0), m_currentCommandIndex(0),
      m_currentCommandFrame(0), m_frameCount(0), m_totalScriptFrames(0) {
    ParseScript(pData);
    
    // Pre-calculate total script frames for efficient looping
    m_totalScriptFrames = 0;
    for (uint16_t i = 0; i < m_commandCount; i++) {
        m_totalScriptFrames += m_commands[i].duration;
    }
}

ScriptReader::~ScriptReader() {
    if (m_commands != nullptr) {
        delete[] m_commands;
    }
}

void ScriptReader::ParseScript(const uint8_t *pData) {
    // Script format (binary):
    // 2 bytes: number of commands (big endian)
    // Then for each command:
    //   2 bytes: duration in frames (big endian)
    //   8 bytes: GCPadStatus structure
    
    // Read command count
    m_commandCount = (pData[0] << 8) | pData[1];
    pData += 2;
    
    // Allocate command array
    m_commands = new ScriptCommand[m_commandCount];
    
    // Parse each command
    for (uint16_t i = 0; i < m_commandCount; i++) {
        // Read duration
        m_commands[i].duration = (pData[0] << 8) | pData[1];
        pData += 2;
        
        // Read pad status (8 bytes)
        memcpy(&m_commands[i].padStatus, pData, sizeof(GCPadStatus));
        pData += sizeof(GCPadStatus);
    }
}

GCPadStatus ScriptReader::CalcFrame(uint16_t frame) {
    // If we're still on the first frame, return A button pressed to close disconnect screen
    if (frame == 0) {
        GCPadStatus ret = s_defaultGCPadStatus;
        ret.a = 1;
        return ret;
    }
    
    // Skip the reconnection period (same as RKG reader)
    constexpr uint16_t FRAMES_AFTER_RECONNECT = 283;
    if (frame < FRAMES_AFTER_RECONNECT) {
        return s_defaultGCPadStatus;
    }
    
    // Adjust frame for reconnection delay to get script-relative frame
    uint16_t scriptFrame = frame - FRAMES_AFTER_RECONNECT;
    
    // Detect if this is a new frame (handles uint16_t wraparound)
    // Only advance state when we detect a new frame
    if (scriptFrame != m_frameCount) {
        uint16_t oldFrameCount = m_frameCount;
        m_frameCount = scriptFrame;
        
        // Calculate how many frames advanced (handles wraparound)
        uint16_t framesAdvanced;
        if (scriptFrame > oldFrameCount) {
            framesAdvanced = scriptFrame - oldFrameCount;
        } else {
            // Wrapped around (uint16_t overflow)
            framesAdvanced = (65535 - oldFrameCount) + scriptFrame + 1;
        }
        
        // Advance by the number of frames that passed
        for (uint16_t f = 0; f < framesAdvanced; f++) {
            m_currentCommandFrame++;
            
            // Check if we've finished the current command
            while (m_currentCommandIndex < m_commandCount && 
                   m_currentCommandFrame >= m_commands[m_currentCommandIndex].duration) {
                m_currentCommandFrame = 0;
                m_currentCommandIndex++;
                
                // AUTO-LOOP: If we've finished all commands, restart from the beginning
                if (m_currentCommandIndex >= m_commandCount) {
                    m_currentCommandIndex = 0;
                    m_currentCommandFrame = 0;
                }
            }
        }
    }
    
    // Return current command's pad status (will always be valid due to auto-loop)
    return m_commands[m_currentCommandIndex].padStatus;
}

