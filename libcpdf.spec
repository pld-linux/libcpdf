Summary:	PDF manipulating library
Summary(pl):	Biblioteka do obróbki plików PDF
Name:		libcpdf
Version:	2.02r1
%define		fileversion 202r1
%define		minorversion 2
Release:	4
License:	Free for non-commercial use
Group:		Libraries
Source0:	http://www.fastio.com/clibpdf%{fileversion}.tar.gz
# Source0-md5: 840d78e187ab46fc5700caba9fbb33e5
Source1:	%{name}-examples.Makefile
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-config.patch
URL:		http://www.fastio.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	zlib-devel
#Requires:	xpdf
#Requires:	ghostscript-fonts-std
#Requires:	ghostscript-fonts-other

%description
This is a library of ANSI C functions, for creating PDF files directly
via C.

%description -l pl
To jest biblioteka funkcji ANSI C do tworzenia plików PDF bezpo¶rednio
z C.

%package devel
Summary:	Header files needed for libcpdf development
Summary(pl):	Pliki nag³ówkowe do programowania z u¿yciem libcpdf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel

%description devel
This package includes the header files for developing programs using
libcpdf.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe potrzebne do programowania z
u¿yciem libcpdf.

%package static
Summary:	Static libraries for libcpdf development
Summary(pl):	Statyczne biblioteki libcpdf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	zlib-devel

%description static
This package includes static libcpdf libraries.

%description static -l pl
Ten pakiet zawiera statyczne biblioteki libcpdf.

%prep
%setup -q -n ClibPDF
%patch0 -p0
%patch1 -p1

cp -f %{SOURCE1} examples/Makefile

%build
cd source
%{__make} -f Makefile.Linux shlib \
	CFLAGS="%{rpmcflags} -DLinux -fPIC" \
	VERSION="%{version}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_bindir},%{_mandir}/man1}

install source/cpdflib.h $RPM_BUILD_ROOT%{_includedir}
install source/libcpdf.so.*.* $RPM_BUILD_ROOT%{_libdir}
(cd $RPM_BUILD_ROOT%{_libdir} ; ln -sf libcpdf.so.*.* libcpdf.so)

install source/libcpdf.a $RPM_BUILD_ROOT%{_libdir}

#cp fontmap.lst $RPM_BUILD_ROOT%{_datadir}/ghostscript/fonts

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -rf examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc source/ChangeLog doc/*.txt fonts/README* LICENSE*
%attr(755,root,root) %{_libdir}/libcpdf.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/*.pdf
%attr(755,root,root) %{_libdir}/libcpdf.so
%{_includedir}/cpdflib.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libcpdf.a
