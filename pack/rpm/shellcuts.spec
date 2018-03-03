# Part of Shellcuts by Tgsachse

### METADATA ###
Name:           shellcuts 

Version:        1.2.1
Release:        1%{?dist}
Summary:        directory shortcuts for your shell

License:        GPLv3
BuildArch:      noarch
BuildRequires:  python3
Requires:       python3
URL:            https://www.github.com/tgsachse/%{name}
Source0:        https://www.github.com/tgsachse/archive/v%{version}.tar.gz


### DEFINES ###
%define share %{buildroot}/usr/share

# Honestly unsure why this line is needed.
%global debug_package %{nil}

%description
Shellcuts are directory shortcuts for your shell. This program allows you to save locations
as 'shellcuts' and then cut back to those locations with a single, short command.


### BUILD PROCESS ###
%prep
%autosetup -n v%{version}

%build
# Compiles core python files.
python3 -m compileall bin/sc-handler.py bin/sc-init.py

%install
rm -rf $RPM_BUILD_ROOT

# Makes the directory structure for the package.
mkdir -p %{share}/man/man1
mkdir -p %{share}/doc/%{name}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{share}/%{name}/zsh
mkdir -p %{share}/%{name}/bash
mkdir -p %{share}/%{name}/fish

# Moves files from their unzipped locations into the directory structure.
install -m 0555 bin/sc %{buildroot}/usr/bin/
install -m 0555 bin/__pycache__/sc-init.cpython-36.pyc %{buildroot}/usr/bin/sc-init
install -m 0555 bin/__pycache__/sc-handler.cpython-36.pyc %{buildroot}/usr/bin/sc-handler

install -m 0444 docs/*.1 %{share}/man/man1/
install -m 0444 docs/*.txt %{share}/doc/%{name}/
install -m 0444 docs/*.rst %{share}/doc/%{name}/

install -m 0444 share/zsh/* %{share}/%{name}/zsh/
install -m 0444 share/bash/* %{share}/%{name}/bash/
install -m 0444 share/fish/* %{share}/%{name}/fish/


### STRUCTURE ###
%files
/usr/bin/sc
/usr/bin/sc-init
/usr/bin/sc-handler

/usr/share/%{name}/*

%doc /usr/share/man/man1/*
%doc /usr/share/doc/%{name}/*

%dir /usr/share/%{name}/
%dir /usr/share/doc/%{name}
%dir /usr/share/%{name}/zsh/
%dir /usr/share/%{name}/bash/
%dir /usr/share/%{name}/fish/

%readme /usr/share/doc/%{name}/README.rst
%license /usr/share/doc/%{name}/LICENSE.txt


### CHANGES ###
%changelog
* Wed Feb 28 2018 Tiger Sachse <tgsachse@gmail.com>
- reorganizing file for clarity
- including support for install source code

* Sat Feb 10 2018 Tiger Sachse <tgsachse@gmail.com>
- preparing for initial release

* Thu Feb  8 2018 Tiger Sachse <tgsachse@gmail.com>
- initial packaging
