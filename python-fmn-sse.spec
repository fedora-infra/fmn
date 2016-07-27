%global pkgname fmn-sse
%global sum Realtime fedmsg feed for fedora users.

Name:           python-%{pkgname}
Version:        0.1
Release:        1%{?dist}
Summary:        %{sum}

License:        GPL
URL:            https://github.com/fedora-infra/fmn.sse
Source0:        https://github.com/fedora-infra/fmn.sse/archive/master.zip

BuildArch:      noarch
BuildRequires:  python-devel

%description
FMN is a family of systems to manage end-user notifications triggered by
fedmsg, the Fedora Federated Message bus.

FMN.SSE allows fedora users to view their fedmsg feed in realtime.

%package -n python2-%{pkgname}
Summary:        %{sum}

Requires:       python-pika
Requires:       python-twisted-web
Requires:       fedmsg
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-twisted
BuildRequires:  python-mock

%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname}
FMN.SSE allows fedora users to view their fedmsg feed in realtime.

%prep
%autosetup -n %{pkgname}-%{version}

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
trial tests/*.py

%files -n python2-%{pkgname}
%doc README.md
%license LICENSE
%{python2_sitelib}/%{pkgname}/
%{python_sitelib}/*.egg-info/

%changelog
* Wed Jul 27 2016 Simon M <skrzepto@gmail.com> - 0.1
- Working on initial spec file

