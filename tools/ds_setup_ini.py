import configparser, sys
p = sys.argv[1]
c = configparser.RawConfigParser(); c.optionxform = str; c.read(p)
def s(sec, k, v):
    if not c.has_section(sec): c.add_section(sec)
    c.set(sec, k, v)
s('Main','SetupWizardIncomplete','false'); s('Main','ConfirmPowerOff','false'); s('Main','SaveStateOnExit','false')
s('AutoUpdater','CheckAtStartup','false')
s('BIOS','SearchDirectory','/home/claude/tmm/tools/bios'); s('BIOS','PatchFastBoot','true')
s('GPU','Renderer','Software')
s('MemoryCards','Card1Type','Shared'); s('MemoryCards','Card1Path','/home/claude/ds/card.mcd')
s('Pad1','Type','DigitalController')
s('Audio','Backend','Null')
with open(p,'w') as f: c.write(f)
