#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	glade3		# Glade 3 support
#
Summary:	Mx Toolkit
Summary(pl.UTF-8):	Toolkit widgetów Mx
Name:		mx
Version:	1.2.1
Release:	1
License:	LGPL v2.1
Group:		X11/Libraries
Source0:	http://source.clutter-project.org/sources/mx/1.2/%{name}-%{version}.tar.xz
# Source0-md5:	2595a61511f3e354eecd4031f6804ac9
URL:		http://www.clutter-project.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	clutter-devel >= 1.4.0
# clutter-imcontext-0.1, clutter-gesture
BuildRequires:	dbus-glib-devel >= 0.82
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 0.6.4
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.35.0
%{?with_glade3:BuildRequires:	libgladeui-devel >= 3.4.5}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	startup-notification-devel >= 0.9
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXrandr-devel >= 1.2.0
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mx is a widget toolkit using Clutter that provides a set of standard
interface elements, including buttons, progress bars, scroll bars and
others. It also implements some standard managers. One other
interesting feature is the possibility setting style properties from a
CSS format file.

%description -l pl.UTF-8
Mx to toolkit widgetów korzystający z biblioteki Clutter,
udostępniający zbiór podstawowych elementów interfejsów graficznych,
w tym przyciski, paski postępu, paski przewijania i inne. Implementuje
także niektórych standardowych zarządców. Interesującą funkcją jest
możliwość ustawiania właściwości styli poprzez plik w formacie CSS.

%package devel
Summary:	Header files for mx libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek mx
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	clutter-devel >= 1.4.0
Requires:	gtk+2-devel >= 2:2.20.0

%description devel
Header files for mx libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek mx.

%package apidocs
Summary:	mx libraries API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek mx
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for mx libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek mx.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules \
	%{?with_glade3:--with-glade} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}-1.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}-1.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mx-create-image-cache
%attr(755,root,root) %{_libdir}/libmx-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmx-1.0.so.2
%attr(755,root,root) %{_libdir}/libmx-gtk-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmx-gtk-1.0.so.0
%{_libdir}/girepository-1.0/Mx-1.0.typelib
%{_libdir}/girepository-1.0/MxGtk-1.0.typelib
%{_datadir}/mx

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmx-1.0.so
%attr(755,root,root) %{_libdir}/libmx-gtk-1.0.so
%{_datadir}/gir-1.0/Mx-1.0.gir
%{_datadir}/gir-1.0/MxGtk-1.0.gir
%{_includedir}/mx-1.0
%{_pkgconfigdir}/mx-1.0.pc
%{_pkgconfigdir}/mx-gtk-1.0.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mx-gtk
%{_gtkdocdir}/mx
%endif
