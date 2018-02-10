Name:           shellcuts 
Version:        1.1.2
Release:        1%{?dist}
Summary:        directory shortcuts for your shell

BuildArch:      noarch
License:        GPL
URL:            https://www.github.com/tgsachse/%{name}
Source0:        https://www.github.com/tgsachse/archive/%{name}-%{version}.tar.gz

BuildRequires:  python3
Requires:       python3

%global debug_package %{nil}

%description
Shellcuts are directory shortcuts for your shell. This program allows you to save locations
as 'shellcuts' and then cut back to those locations with a single, short command.

%prep
%setup -q

%build
python3 -m compileall bin/sc-handler.py bin/sc-init.py

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/%{name}
mkdir -p %{buildroot}/usr/share/man/man1
mkdir -p %{buildroot}/usr/share/doc/%{name}

install -m 0555 bin/__pycache__/sc-handler.cpython-36.pyc %{buildroot}/usr/bin/sc-handler
install -m 0555 bin/__pycache__/sc-init.cpython-36.pyc %{buildroot}/usr/bin/sc-init

install -m 0444 docs/*.txt %{buildroot}/usr/share/doc/%{name}/
install -m 0444 docs/*.rst %{buildroot}/usr/share/doc/%{name}/
install -m 0444 docs/*.1 %{buildroot}/usr/share/man/man1/

install -d share/* %{buildroot}/usr/share/%{name}/

%files
%license /usr/share/doc/%{name}/LICENSE.txt
%doc /usr/share/doc/%{name}/*
%doc /usr/share/man/man1/*
%dir /usr/share/%{name}
%dir /usr/share/doc/%{name}
/usr/bin/sc-handler
/usr/bin/sc-init

%changelog
* Thu Feb  8 2018 Tiger Sachse <tgsachse@gmail.com>
- initial packaging
