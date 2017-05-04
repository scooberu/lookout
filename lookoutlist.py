#author: Scott Reu (sreu@cisco.com)

from lookout import Fmc

#Reminder: Fmc class default order + values:
#hostname=None, ipaddr=None, username='', passwd='', status='ok'

rtpFMC = Fmc('Lookout_RTP_FMC', '172.18.124.211', 'admin', 'S0urceF!reRTP')
sjFMC = Fmc('Lookout_SJ_FMC', '172.16.53.4', 'admin', 'S0urceF!reSJ')
#krkFMC = Fmc('Lookout_KRK_FMC', '172.16.53.4', 'admin', 'S0urceF!reKRK')
bglFMC = Fmc('Lookout_BGL_FMC', '10.76.77.20', 'admin', 'S0urceF!reBGL')
bruFMC = Fmc('Lookout_BRU_FMC', '10.48.18.41', 'admin', 'S0urceF!reBRU')

fmclist = [rtpFMC,sjFMC,bglFMC,bruFMC]
