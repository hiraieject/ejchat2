help:
	# make install		インストール

DIRS = lock users profiles

install:
	@for dir in `echo $(DIRS)`; \
		do mkdir -p $$dir; \
		echo "Deny from all" > $$dir/.htaccess; \
	done
	mkdir -p log archive
	chmod 644 *
	find . -type d -exec chmod uo+rwx {} \;
	find . -name \*.cgi -exec chmod uo+rx {} \;
	if [ ! -f log/message.html ] ; then \
		touch log/message.html; chmod o+w log/message.html;\
		echo "<SCRIPT LANGUAGE=\"JavaScript\">" >> log/message.html;\
		echo "var mes_mtime=0;" >> log/message.html;\
		echo "</SCRIPT>" >> log/message.html;\
	fi

tar:
	rm -r chat; mkdir -p chat
	cp *.cgi *.pl *.html Makefile chat/
	cp -r CVS chat/
	tar cvfz ejchat2.current.tar.gz chat
	rm -rf chat
	cp *.tar.gz archive

release:
	@make tar
	cp ejchat2.current.tar.gz ejchat2.v`head -1 version.txt | awk '{print $$3}'`.tar.gz
	mv *.tar.gz archive
	ls -l archive/

