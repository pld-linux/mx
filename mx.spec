#
# Conditional build:
%bcond_without	apidocs		# gtk-doc based API documentation
%bcond_with	glade3		# Glade 3 support
%bcond_without	imcontext	# Clutter input method support
%bcond_without	gesture		# Clutter Gesture support

Summary:	Mx Toolkit
Summary(pl.UTF-8):	Toolkit widgetów Mx
Name:		mx
Version:	1.4.7
Release:	10
License:	LGPL v2.1
Group:		X11/Libraries
Source0:	https://github.com/downloads/clutter-project/mx/%{name}-%{version}.tar.xz
# Source0-md5:	19b1e4918a5ae6d014fc0dab2bb3d0a1
Patch0:		gdk-pixbuf.patch
Patch1:		0001-Replace-GL-data-types-with-equivalent-glib-types.patch
URL:		http://www.clutter-project.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	clutter-devel >= 1.8.0
%{?with_gesture:BuildRequires:	clutter-gesture-devel}
%{?with_imcontext:BuildRequires:	clutter-imcontext-devel >= 0.1}
BuildRequires:	dbus-glib-devel >= 0.82
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gobject-introspection-devel >= 0.6.4
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.35.0
%{?with_glade3:BuildRequires:	libgladeui-devel >= 3.4.5}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	startup-notification-devel >= 0.9
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXrandr-devel >= 1.2.0
BuildRequires:	xz
Requires:	clutter >= 1.8.0
Requires:	dbus-glib >= 0.82
Requires:	glib2 >= 1:2.28.0
Requires:	gtk+2 >= 2:2.20.0
Requires:	startup-notification >= 0.9
Requires:	xorg-lib-libXrandr >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mx is a widget toolkit using Clutter that provides a set of standard
interface elements, including buttons, progress bars, scroll bars and
others. It also implements some standard managers. One other
interesting feature is the possibility setting style properties from a
CSS format file.

%description -l pl.UTF-8
Mx to toolkit widgetów korzystający z biblioteki Clutter,
udostępniający zbiór podstawowych elementów interfejsów graficznych, w
tym przyciski, paski postępu, paski przewijania i inne. Implementuje
także niektórych standardowych zarządców. Interesującą funkcją jest
możliwość ustawiania właściwości styli poprzez plik w formacie CSS.

%package devel
Summary:	Header files for mx libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek mx
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	clutter-devel >= 1.8.0
Requires:	dbus-glib-devel >= 0.82
Requires:	gdk-pixbuf2-devel
Requires:	glib2-devel >= 1:2.28.0
Requires:	gtk+2-devel >= 2:2.20.0
Requires:	startup-notification-devel >= 0.9
Requires:	xorg-lib-libXrandr-devel >= 1.2.0
%if %{without glade3}
Obsoletes:	glade3-mx < %{version}-%{release}
%endif

%description devel
Header files for mx libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek mx.

%package apidocs
Summary:	mx libraries API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek mx
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API documentation for mx libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek mx.

%package -n glade3-mx
Summary:	MX catalog file for Glade3
Summary(pl.UTF-8):	Plik katalogu MX dla Glade3
Group:		Development/Tools
Requires:	%{name}-devel = %{version}-%{release}
Requires:	glade3 >= 3.4.5

%description -n glade3-mx
MX catalog file for Glade3.

%description -n glade3-mx -l pl.UTF-8
Plik katalogu MX dla Glade3.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules \
	--with-clutter-gesture%{!?with_gesture:=no} \
	--with-clutter-imcontext%{!?with_imcontext:=no} \
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

%if %{with glade3}
%files -n glade3-mx
%defattr(644,root,root,755)
%{_datadir}/glade3/catalogs/mx-gtk-catalog.xml
%endif
