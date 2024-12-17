import pcbnew 
def adjust_power_net_track_width(new_width, net_name="+15"): 
	board = pcbnew.GetBoard() 
	for track in board.GetTracks(): 
		if hasattr(track, 'GetNetname') and track.GetNetname() == net_name: 
			track.SetWidth(pcbnew.FromMM(new_width)) 
	pcbnew.Refresh() 
# Example usage: Set the track width for the power net to 0.5mm
adjust_power_net_track_width(0.5)