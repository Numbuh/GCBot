#pragma once

#include "GCPadStatus.hpp"

#include <cstddef>
#include <cstdint>

struct ScriptCommand {
    uint16_t duration;      // How many frames this command lasts
    GCPadStatus padStatus;  // The controller state for this command
};

class ScriptReader {
public:
    ScriptReader(const uint8_t *pData);
    ~ScriptReader();

    GCPadStatus CalcFrame(uint16_t frame);

private:
    void ParseScript(const uint8_t *pData);
    
    ScriptCommand *m_commands;
    uint16_t m_commandCount;
    uint16_t m_currentCommandIndex;
    uint16_t m_currentCommandFrame;  // Which frame within the current command
    uint16_t m_frameCount;           // Total frames processed (unused with new logic, kept for compatibility)
    uint16_t m_totalScriptFrames;    // Total frames in script (pre-calculated for efficient looping)
};

