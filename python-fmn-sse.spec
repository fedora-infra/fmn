%global pkgname fmn-sse
%global modname fmn.sse
%global sum FMN.SSE allows fedora users to view their fedmsg feed in realtime.

Name:           python-%{pkgname}
Version:        0.1.0
Release:        1%{?dist}
Summary:        %{sum}

License:        GPL
URL:            https://github.com/fedora-infra/%{modname}
Source0:        https://github.com/fedora-infra/%{modname}/archive/v%{version}.zip

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-mock
BuildRequires:  python-twisted
BuildRequires:  python-pika
BuildRequires:  fedmsg
BuildRequires:  python-pytest
BuildRequires:  systemd
BuildRequires:  systemd-devel

Requires:       python-pika
Requires:       fedmsg
Requires:       python-twisted

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
FMN is a family of systems to manage end-user notifications triggered by
fedmsg, the Fedora Federated Message bus.

%{sum}

Summary:        %{sum}

%description
FMN.SSE allows fedora users to view their fedmsg feed in realtime.

%prep
%autosetup -n %{modname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{pkgname}.egg-info

%build
%py2_build

%install
%py2_install

# Install the systemd files
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
install -m 644 systemd/fmn-sse@.service \
    $RPM_BUILD_ROOT/%{_unitdir}/fmn-sse@.service

%check
%{__python2} setup.py test

%files
%doc README.md
%license LICENSE
%{python2_sitelib}/fmn/__init__.py*
%{python2_sitelib}/fmn/sse/
%{python2_sitelib}/%{modname}-%{version}*
%{_unitdir}/fmn-sse@.service

%changelog
* Wed Jul 27 2016 Simon M <skrzepto@gmail.com> - 0.1
- Working on initial spec file
