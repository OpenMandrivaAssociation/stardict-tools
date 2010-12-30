%define version 3.0.1
%define release %mkrel 4

Summary:	Some tools for StarDict
Name:		stardict-tools
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Text tools
URL:		http://stardict.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

Source:		http://stardictproject.googlecode.com/files/%{name}-%{version}.tar.bz2
Patch0:		%{name}-3.0.1-fix-underlinking.patch
Patch1:		%{name}-3.0.1-fix-gcc43.patch
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

%build
autoreconf -f -i
%configure
%make

%install
rm -rf %{buildroot}
%makeinstall

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL
%doc NEWS README
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/applications/*.desktop

