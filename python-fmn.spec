%global srcname fmn

# python-sqlalchemy_schemadisplay is not yet in Fedora
# https://bugzilla.redhat.com/show_bug.cgi?id=1409929
%global with_docs 0

Name:           python-%{srcname}
Version:        2.4.0
Release:        1%{?dist}
Summary:        A system for generic fedmsg-driven notifications for end users

License:        LGPLv2+
URL:            https://github.com/fedora-infra/%{srcname}
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description
fmn is a family of systems to manage end-user notifications triggered by
fedmsg, the FEDerated MESsage bus. fmn provides a single place for all
applications using fedmsg to notify users of events. Notifications can be
delivered by email, IRC, and server-sent events. Users can configure their
notifications for all the applications they use in one place.

%package -n python3-%{srcname}
Summary:        %{summary}
Requires:           httpd
%{?systemd_ordering}

BuildRequires:      python3-arrow
BuildRequires:      python3-beautifulsoup4
BuildRequires:      python3-bleach
BuildRequires:      python3-munch
BuildRequires:      python3-celery
BuildRequires:      python3-datanommer-models
BuildRequires:      python3-devel
BuildRequires:      python3-docutils
BuildRequires:      python3-dogpile-cache
BuildRequires:      python3-fedmsg
BuildRequires:      python3-fedmsg-meta-fedora-infrastructure
BuildRequires:      python3-fedora
BuildRequires:      python3-flake8
BuildRequires:      python3-flask
BuildRequires:      python3-flask-openid
BuildRequires:      python3-html5lib
BuildRequires:      python3-markupsafe
BuildRequires:      python3-moksha-hub
BuildRequires:      python3-mock
BuildRequires:      python3-openid
BuildRequires:      python3-openid-cla
BuildRequires:      python3-openid-teams
BuildRequires:      python3-pika
BuildRequires:      python3-pylibravatar
BuildRequires:      python3-pytest
BuildRequires:      python3-redis
BuildRequires:      python3-requests
BuildRequires:      python3-setuptools
BuildRequires:      python3-six
BuildRequires:      python3-sqlalchemy >= 0.8
BuildRequires:      python3-twisted
BuildRequires:      python3-vcrpy
BuildRequires:      python3-wtforms
BuildRequires:      python3-devel
BuildRequires:      systemd-rpm-macros
%{?python_provide:%python_provide python3-%{srcname}}

Provides: python-fmn-rules = %{version}-%{release}
Obsoletes: python-fmn-rules < 0.9.1-2%{?dist}
Provides: python-fmn-lib = %{version}-%{release}
Obsoletes: python-fmn-lib < 0.8.2-3%{?dist}
Provides: python-fmn-consumer = %{version}-%{release}
Obsoletes: python-fmn-consumer < 1.0.3-2%{?dist}
Provides: python-fmn-web = %{version}-%{release}
Obsoletes: python-fmn-web < 0.8.1-4%{?dist}
Provides: python-fmn-sse = %{version}-%{release}
Obsoletes: python-fmn-sse < 0.2.1-4%{?dist}

%description -n python3-%{srcname}
fmn is a family of systems to manage end-user notifications triggered by
fedmsg, the FEDerated MESsage bus. fmn provides a single place for all
applications using fedmsg to notify users of events. Notifications can be
delivered by email, IRC, and server-sent events. Users can configure their
notifications for all the applications they use in one place.


%if 0%{?with_docs} > 0
%package doc
Summary:        HTML documentation for python-fmn
BuildRequires:  make
BuildRequires:  python3-sphinx
BuildRequires:  python3-sqlalchemy_schemadisplay

%description -n python-%{srcname}-doc
HTML documentation for python-fmn.
%endif


%prep
%autosetup -p1 -n %{srcname}-%{version}
sed -i -e 's|^python-openid$|python3-openid|' requirements.txt
sed -i -e 's|fedmsg\[consumers, commands\]||' requirements.txt
cat requirements.txt


%build
%py3_build


%if 0%{?with_docs} > 0
pushd docs
PYTHONPATH=$(dirname $(pwd)) make html
popd
%endif


%install
%py3_install


install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_datadir}/%{srcname}
install -pm644 alembic.ini %{buildroot}/%{_datadir}/%{srcname}/alembic.ini
install -pm644 systemd/fmn-backend@.service %{buildroot}/%{_unitdir}/
install -pm644 systemd/fmn-celerybeat.service %{buildroot}/%{_unitdir}/
install -pm644 systemd/fmn-worker@.service %{buildroot}/%{_unitdir}/
cp -a alembic %{buildroot}/%{_datadir}/%{srcname}/

%{__mkdir_p} %{buildroot}/%{_datadir}/%{srcname}
%{__mkdir_p} %{buildroot}/%{_sysconfdir}/httpd/conf.d
cp -p apache/%{srcname}.web.wsgi %{buildroot}%{_datadir}/%{srcname}/%{srcname}.web.wsgi
cp -p apache/%{srcname}.web.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{srcname}.web.conf
cp -r fmn/web/static/ %{buildroot}%{_datadir}/%{srcname}/static

cp -p usr/share/fmn/delivery_service.tac %{buildroot}%{_datadir}/%{srcname}/delivery_service.tac
cp -p usr/share/fmn_sse/sse_server.tac %{buildroot}%{_datadir}/%{srcname}/sse_server.tac

rm -rf %{buildroot}%{_datadir}/%{srcname}/static/bootstrap


%check
# Tests aren't shipped in the tarball
#PYTHONPATH=$(pwd) pytest-3


%files -n python3-%{srcname}
%license COPYING COPYING.LESSER
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/*
%{_datadir}/%{srcname}
%{_bindir}/fmn-createdb
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{srcname}.web.conf


%if 0%{?with_docs} > 0
%files doc
%license COPYING COPYING.LESSER
%doc README.rst CHANGELOG.rst docs/_build/html/
%endif


%changelog
* Wed Jun 15 2022 Michal Konecny <mkonecny@redhat.com> - 2.4.0-1
- Update to 2.4.0
- Cleanup of systemd units
- Make the FMN work in Fedora 36

* Fri Mar 4 2022 Michal Konecny <mkonecny@redhat.com> - 2.3.0-1
- Update to 2.3.0
- Remove links to old website
- Remove the archived repositories from documentation
- Use fasjson library
- Make the FMN work in Fedora 34

* Fri Sep 17 2021 Stephen Coady <scoady@redhat.com> - 2.2.3-1
- Update to 2.2.3
- Fix config accessor for fasjson
- Actually use the datanommer.enabled config flag

* Mon May 10 2021 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.2.2-3
- Fix sed command

* Mon May 10 2021 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.2.2-2
- Tweak the requirements.txt file

* Fri May 07 2021 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.2.2-1
- Update to 2.2.2

* Fri May 07 2021 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.2.1-1
- Update to 2.2.1
- Drop dependency on pydns
- Change dependency from bunch to munch

* Fri May 07 2021 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.2.0-1
- Update to 2.2.0
- Port the package to python3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 05 2018 Jeremy Cline <jeremy@jcline.org> - 2.1.1-1
- Update to latest upstream

* Tue Apr 03 2018 Jeremy Cline <jeremy@jcline.org> - 2.1.0-2
- Fix a bug in the latest database migration

* Tue Apr 03 2018 Jeremy Cline <jeremy@jcline.org> - 2.1.0-1
- Update to latest upstream

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.2-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Jeremy Cline <jeremy@jcline.org> - 2.0.2-2
- Just bump the spec to match f27

* Fri Jan 12 2018 Jeremy Cline <jeremy@jcline.org> - 2.0.2-1
- Update to latest upstream

* Thu Nov 02 2017 Jeremy Cline <jeremy@jcline.org> - 2.0.1-1
- Update to latest upstream

* Wed Oct 25 2017 Jeremy Cline <jeremy@jcline.org> - 2.0.0-2
- Drop the runtime dependency on vcrpy

* Wed Oct 25 2017 Jeremy Cline <jeremy@jcline.org> - 2.0.0-1
- Update to latest upstream

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Jeremy Cline <jeremy@jcline.org> - 1.3.1-2
- Add a missing dependency (python-bunch)

* Mon Jun 12 2017 Jeremy Cline <jeremy@jcline.org> - 1.3.1-1
- Update to latest upstream

* Wed May 31 2017 Jeremy Cline <jeremy@jcline.org> - 1.3.0-1
- Update to 1.3.0
- Provide fmn-sse and fmn-web

* Mon Apr 10 2017 Jeremy Cline <jeremy@jcline.org> - 1.2.0-1
- Update to upstream 1.2.0

* Fri Jan 20 2017 Jeremy Cline <jeremy@jcline.org> - 1.1.0-1
- Update to latest upstream
- Address package review comments

* Thu Jan 05 2017 Jeremy Cline <jeremy@jcline.org> - 1.0.0-1
- Initial package.
