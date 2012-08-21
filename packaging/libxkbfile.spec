Summary: X.Org X11 libxkbfile runtime library
Name: libxkbfile
Version: 1.0.8
Release: 1
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: %{name}-%{version}.tar.gz

BuildRequires: pkgconfig(xproto) pkgconfig(x11)
BuildRequires: pkgconfig(xorg-macros)

%description
X.Org X11 libxkbfile runtime library

%package devel
Summary: X.Org X11 libxkbfile development package
Group: Development/Libraries
Provides: libxkbfile-devel 
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libxkbfile development package

%prep
%setup -q

%build
# FIXME: We use -fno-strict-aliasing, to work around the following bug:
# maprules.c:1373: warning: dereferencing type-punned pointer will break strict-aliasing rules)
export CFLAGS="${CFLAGS} $RPM_OPT_FLAGS -fno-strict-aliasing"
%reconfigure --disable-static \
	       LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"
make %{?jobs:-j%jobs}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%{_libdir}/libxkbfile.so.1
%{_libdir}/libxkbfile.so.1.0.2

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/XKBbells.h
%{_includedir}/X11/extensions/XKBconfig.h
%{_includedir}/X11/extensions/XKBfile.h
%{_includedir}/X11/extensions/XKBrules.h
%{_includedir}/X11/extensions/XKM.h
%{_includedir}/X11/extensions/XKMformat.h
%{_libdir}/libxkbfile.so
%{_libdir}/pkgconfig/xkbfile.pc
