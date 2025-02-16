Summary:	Some tools for StarDict
Name:		stardict-tools
Version:	3.0.1
Release:	8
License:	GPLv2+
Group:		Text tools
URL:		https://stardict.sourceforge.net/

Source:		http://stardictproject.googlecode.com/files/%{name}-%{version}.tar.bz2
Patch0:		%{name}-3.0.1-fix-underlinking.patch
Patch1:		%{name}-3.0.1-fix-gcc43.patch
Patch2:		stardict-tools-3.0.1-fix-gcc45.patch
BuildRequires:	libpcre-devel
BuildRequires:	gtk+2-devel
BuildRequires:	mysql-devel
BuildRequires:	stardict
Requires:	stardict

%description
This package contain some tools for StarDict, an international dictionary.

%prep
%setup -q
%patch0 -p1 -b .undlink
%patch1 -p1 -b .gcc43
%patch2 -p1 -b .gcc45

%build
export LDFLAGS="-lz"
autoreconf -f -i
%configure2_5x
%make

%install
%makeinstall_std

# finish install
mkdir -p %{buildroot}%{_libdir}/%{name}
pushd src
grep noinst_PROGRAMS Makefile.am > tmplist
perl -pi -e 's/noinst\_PROGRAMS \= //' tmplist
	for i in `cat tmplist`; do
		cp $i %{buildroot}%{_libdir}/%{name}/$i
	done
rm -f tmplist
popd

# menu entry
mkdir -p %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/stardict-editor.desktop
[Desktop Entry]
Encoding=UTF-8
Name=StarDict Editor
Comment=Editor for StarDict
Exec=stardict-editor
Icon=stardict
StartupNotify=true
Categories=Utility;Dictionary;Office;GTK;
EOF

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL
%doc NEWS README
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/applications/*.desktop



%changelog
* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-6mdv2011.0
+ Revision: 645898
- relink against libmysqlclient.so.18

* Sun Jan 02 2011 Funda Wang <fwang@mandriva.org> 3.0.1-5mdv2011.0
+ Revision: 627486
- fix build with gcc 4.5

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against mysql-5.5.8 libs, again
    - rebuilt against mysql-5.5.8 libs

* Mon Jun 01 2009 Jérôme Brenier <incubusss@mandriva.org> 3.0.1-2mdv2010.0
+ Revision: 382012
- import stardict-tools


