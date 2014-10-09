# based on PLD Linux spec git://git.pld-linux.org/packages/parted.git
Summary:	Flexible partitioning tool
Name:		parted
Version:	3.2
Release:	1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
# Source0-md5:	0247b6a7b314f8edeb618159fa95f9cb
Source1:	%{name}.m4
URL:		http://www.gnu.org/software/parted/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel
BuildRequires:	gettext-devel
BuildRequires:	libblkid-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags		-fgnu89-inline
%define		skip_post_check_so	libparted-fs-resize.so.*

%description
GNU Parted is a program that allows you to create, destroy, resize,
move and copy hard disk partitions. This is useful for creating space
for new operating systems, reorganising disk usage, and copying data
to new hard disks.

%package libs
Summary:	libparted library
Group:		Libraries

%description libs
libparted library.

%package devel
Summary:	Files required to compile software that uses libparted
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	device-mapper-devel
Requires:	pkgconfig(blkid)
Requires:	pkgconfig(libcryptsetup)

%description devel
Files required to compile software that uses libparted.

%prep
%setup -q

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--with-readline		\
	--disable-static	\
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	aclocaldir=%{_aclocaldir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

install -D %{SOURCE1} $RPM_BUILD_ROOT%{_aclocaldir}/parted.m4

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/{API,FAT} AUTHORS BUGS ChangeLog NEWS README THANKS TODO
%lang(ja) %doc doc/USER.jp
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%{_infodir}/parted*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_aclocaldir}/*
%{_includedir}/parted
%{_pkgconfigdir}/libparted.pc

