%define _prefix /var/opt/mkcdrec
%define _webmin_root /usr/libexec/webmin
%define _webmin_access_file /etc/webmin/webmin.acl
%define _webmin_cache_cile /etc/webmin/module.infos.cache
%define _boot_arch x86
Summary:	mkCDrec (make CD-ROM Recovery) disaster recovery tool-set
Summary(pl):	mkCDrec (zrób CD-ROM odzyskyj±cy system)
Name:		mkcdrec
Version:	0.8.9
Release:	0.1
Source0:	http://mkcdrec.ota.be/project/mkCDrec_v%{version}.tar.gz
# Source0-md5:	0cbe2efbd083ce9745c5d5c5cea1c7c2
##Source1: busybox-1.01.tar.bz2
URL:		http://mkcdrec.ota.be/
License:	GPL
Group:		System/Tools
Provides:	perl(mkcdrec-lib.pl)
Requires:	MAKEDEV

%if %{_boot_arch}==ia64
Prereq:		chkconfig fileutils cdrecord mkisofs tar ash mtools rsync
Requires:	kernel >= 2.0.0, util-linux >= 2.11, perl >= 5.0, parted >= 1.6
BuildRequires:	gcc >= 2.96
%endif
%if %{_boot_arch}==x86_64
Prereq:		fileutils cdrecord mkisofs tar ash rsync syslinux
Requires:	kernel >= 2.0.0, util-linux >= 2.11, perl >= 5.0
BuildRequires:	gcc >= 2.96
%endif
%if %{_boot_arch}==x86
Prereq:		coreutils fileutils cdrecord mkisofs tar ash syslinux rsync
Requires:	kernel >= 2.0.0, util-linux >= 2.11, perl >= 5.0
BuildRequires:	syslinux >= 1.60, gcc >= 2.96
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mkCDrec (Make CDROM Recovery) makes a bootable (El Torito) disaster
recovery image, including backups of the Linux system to one or more
CD-ROM(s) (multi-volume sets). Otherwise, the backups can be stored on
another disk, NFS disk, or (remote) tape. After a disk crash or system
intrusion, the system can be booted from the CD-ROM and one can
restore the complete system as it was. It also features disk cloning,
which allows one to restore a disk to another disk (the destination
disk does not have to be of the same size, as it calculates the
partition layout itself). Currently, ext2, ext3, minix, msdos, fat,
vfat, reiserfs, xfs and jfs filesystems are supported. One Button
Disaster Recovery (OBDR) is also supported as recovery method.

%description -l pl
mkCDrec (zrób odzyskuj±cy CDROM) tworzy uruchamialn± (El Torito)
p³tkê zawieraj± system oraz kilka voluminów kopii danych. Zamiast 
wielu p³ytek mo¿na pos³u¿yæ siê innym dyskiem, NFSem, kopi± na ta¶mie.
Po awarii system albo wej¶ciu intruza system mo¿e byæ uruchomiony 
z p³ytki i przywrócony do pierwotnego stanu.
mkcdrec wspiera klonowanie systemu. Aktualnie mo¿na u¿ywaæ ext2, ext3, 
minix, msdos, fat, vfat, reiserfs, xfs and jfs jako systemów plików.
Metoda zwana 'One Button Disaster Recovery (OBDR)' jest równie¿ wpierana.

%prep
%setup -q -n mkcdrec
##%setup -n mkcdrec -a 1

%build
%{__make} -f Makefile.%{_boot_arch} build

%install
rm -rf $RPM_BUILD_ROOT
find . -name CVS | xargs rm -Rfv

install -d $RPM_BUILD_ROOT%{_prefix}/busybox/applets
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_prefix}/contributions
install -d $RPM_BUILD_ROOT%{_prefix}/modules
install -d $RPM_BUILD_ROOT%{_prefix}/scripts/messages
install -d $RPM_BUILD_ROOT%{_prefix}/doc
install -d $RPM_BUILD_ROOT%{_prefix}/doc/style
install -d $RPM_BUILD_ROOT%{_prefix}/doc/images
install -d $RPM_BUILD_ROOT%{_prefix}/usr
install -d $RPM_BUILD_ROOT%{_prefix}%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man8
for fname in busybox*/busybox  busybox*/busybox.links; do
	install -m 755 $fname $RPM_BUILD_ROOT%{_prefix}/busybox
done

install -m 755 busybox*/applets/install.sh $RPM_BUILD_ROOT%{_prefix}/busybox/applets

for fname in  cutstream*/cutstream \
 pastestream*/pastestream mediacheck/checkisomd5 mediacheck/implantisomd5
do
	install -m 755 $fname $RPM_BUILD_ROOT%{_bindir}
done
for fname in contributions/*.sh contributions/mkcdrec; do
	install -m 755 $fname $RPM_BUILD_ROOT%{_prefix}/contributions
done
for fname in scripts/messages/*; do
	install -m 755 $fname $RPM_BUILD_ROOT%{_prefix}/scripts/messages
done
for fname in `find scripts -type f`; do
	install -m 755 $fname $RPM_BUILD_ROOT%{_prefix}/$fname
done
for fname in modules/*; do
	install -m 755 $fname $RPM_BUILD_ROOT%{_prefix}/modules
done
for fname in doc/*.html doc/*.gif doc/*.jpg doc/*.png; do
	install -m 755  $fname $RPM_BUILD_ROOT%{_prefix}/doc
done
for fname in doc/style/*.css; do
	install -m 755  $fname $RPM_BUILD_ROOT%{_prefix}/doc/style
done
for fname in doc/images/*; do
        install -m 755  $fname $RPM_BUILD_ROOT%{_prefix}/doc/images
done

for fname in `find etc -type d`; do
	install -d -m 755  $fname $RPM_BUILD_ROOT%{_prefix}/$fname
done
for fname in `find etc -type f`; do
	install -m 755  $fname $RPM_BUILD_ROOT%{_prefix}/$fname
done
for fname in `find usr -type d`; do
	install -d -m 755  $fname $RPM_BUILD_ROOT%{_prefix}/$fname
done
for fname in `find usr -type f`; do
	install -m 755  $fname $RPM_BUILD_ROOT%{_prefix}/$fname
done

for fname in `find . -type f -maxdepth 1`; do
	install -m 755  $fname $RPM_BUILD_ROOT%{_prefix}/$fname
done

install -m 755 doc/mkcdrec.8 $RPM_BUILD_ROOT%{_mandir}/man8

gzip -c $RPM_BUILD_ROOT%{_mandir}/man8/mkcdrec.8 > \
	$RPM_BUILD_ROOT%{_mandir}/man8/mkcdrec.8.gz

for file in \
    $RPM_BUILD_ROOT%{_prefix}/.cvsignore \
    $RPM_BUILD_ROOT%{_prefix}/COPYING \
    $RPM_BUILD_ROOT%{_prefix}/Changelog \
    $RPM_BUILD_ROOT%{_prefix}/README \
; do rm -f $file ; done

# installation of webmin module


[ ! -d $RPM_BUILD_ROOT%{_webmin_root}/mkcdrec ] && install -d -m 755 $RPM_BUILD_ROOT%{_webmin_root}/mkcdrec
# we copy files in webmin directory
#if test -d $RPM_BUILD_ROOT%{_webmin_root}

	for fname in `find webmin -type d`; do
		install -d -m 755 $fname $RPM_BUILD_ROOT%{_webmin_root}/`echo $fname | sed -e 's/webmin/mkcdrec/'`
	done
	for fname in `find webmin -type f`; do
		install -m 755 $fname $RPM_BUILD_ROOT%{_webmin_root}/`echo $fname | sed -e 's/webmin/mkcdrec/'`
	done
#fi
%files
%defattr(644,root,root,755)
%doc Changelog README COPYING
%doc %{_prefix}/doc
%config %{_prefix}/Config.sh
%{_prefix}/VERSION
%{_prefix}/.config.bb
%{_prefix}/busybox
%attr(755,root,root) %{_bindir}
%{_prefix}/contributions
%{_prefix}/scripts
%{_prefix}/modules
%{_prefix}%{_sysconfdir}
%{_prefix}/usr
%{_prefix}/linuxrc
%{_prefix}/linuxrc_find_and_prep_root
%{_prefix}/linuxrc_post
%{_prefix}/linuxrc_pre
%{_prefix}/Makefile
%{_prefix}/Makefile.new-powermac
%{_prefix}/Makefile.x86
%{_prefix}/Makefile.sparc
%{_prefix}/Makefile.ia64
%{_prefix}/Makefile.x86_64
%{_mandir}/man8/*
%{_webmin_root}/mkcdrec/help.cgi
%{_webmin_root}/mkcdrec/images/icon
%{_webmin_root}/mkcdrec/images/icon.gif
%{_webmin_root}/mkcdrec/index.cgi
%{_webmin_root}/mkcdrec/lang/en
%{_webmin_root}/mkcdrec/lang/fr
%{_webmin_root}/mkcdrec/mkcdrec-lib.pl
%{_webmin_root}/mkcdrec/module.info
%{_webmin_root}/mkcdrec/save.cgi
%{_webmin_root}/mkcdrec/README.webmin

%post
#we add mkcdrec in webmin root's ACL
if [ -f %{_webmin_access_file} ]; then
	cp %{_webmin_access_file} %{_webmin_access_file}.beforemkcdrec.sauv
	ed %{_webmin_access_file} << EOF > /tmp/mkcdrec.log 2>&1
/root:
s/root:/root: mkcdrec/
w
q
EOF
else
	echo "WARNING: it seems that webmin isn't installed on that system.If you install it later, don't forget to add mkcdrec to the list of modules in %{_webmin_access_file} to make mkcdrec's webmin module available."

fi
# install the mkcdrec wrapper
install -m 750 %{_prefix}/contributions/mkcdrec /usr/sbin/mkcdrec

%postun
# we remove mkcdrec from webmin root's ACL

if [ -f %{_webmin_access_file} ]; then
	ed %{_webmin_access_file} << EOF > /tmp/mkcdrec.log 2>&1
s/mkcdrec//g
w
q
EOF
fi
# rm the mkcdrec wrapper
rm -f /usr/sbin/mkcdrec
