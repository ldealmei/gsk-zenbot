def grant_access(my_zenbotid, access_for_zenbotid, access_to_zenbotid, level = 'level3'):
	print(access_to_zenbotid in master_zenbot_dict)
	zenbot = master_zenbot_dict.get(access_to_zenbotid)
	print(zenbot)
	if my_zenbotid in zenbot.accessdict['level1']:
		if level != 'level1':
			zenbot.accessdict[level].append(access_for_zenbotid)
	elif my_zenbotid in zenbot.accessdict['level2']:
		if level not in ['level1', 'level2']:
			zenbot.accessdict[level].append(access_for_zenbotid)
	else:
		print('You are not permitted to grant access to {}.'.format(access_to_zenbotid))


grant_access('Z3N', 'Z3N', zen.zenbotid)
