Summary:	PDF manipulating library
Summary(pl.UTF-8):	Biblioteka do obróbki plików PDF
Name:		libcpdf
Version:	2.02r1
Release:	7
License:	Free for non-commercial use
Group:		Libraries
Source0:	http://www.fastio.com/clibpdf202r1.tar.gz
# Source0-md5:	840d78e187ab46fc5700caba9fbb33e5
Source1:	%{name}-examples.Makefile
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-config.patch
URL:		http://www.fastio.com/
BuildRequires:	zlib-devel
#Requires:	ghostscript-fonts-other
#Requires:	ghostscript-fonts-std
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a library of ANSI C functions, for creating PDF files directly
via C.

%description -l pl.UTF-8
To jest biblioteka funkcji ANSI C do tworzenia plików PDF bezpośrednio
z C.

%package devel
Summary:	Header files needed for libcpdf development
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania z użyciem libcpdf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel

%description devel
This package includes the header files for developing programs using
libcpdf.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do programowania z
użyciem libcpdf.

%package static
Summary:	Static libraries for libcpdf development
Summary(pl.UTF-8):	Statyczne biblioteki libcpdf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	zlib-devel

%description static
This package includes static libcpdf libraries.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczne biblioteki libcpdf.

%prep
%setup -q -n ClibPDF
%patch0 -p0
%patch1 -p1

cp -f %{SOURCE1} examples/Makefile

%build
%{__make} -C source -f Makefile.Linux shlib \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DLinux -fPIC" \
	LDFLAGS="%{rpmldflags}" \
	VERSION="%{version}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_bindir},%{_mandir}/man1}

install source/cpdflib.h $RPM_BUILD_ROOT%{_includedir}
install source/libcpdf.so.*.* $RPM_BUILD_ROOT%{_libdir}
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libcpdf.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libcpdf.so
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
