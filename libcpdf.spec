Summary:	PDF manipulating library
Name:		libcpdf
Version:	2.02r1
%define    fileversion 202r1
%define    minorversion 2
Release:	0
URL:		http://www.fastio.com
Source0:	http://www.fastio.com/clibpdf%{fileversion}.tar.gz
Source1:	cpdfman110.pdf
Source2:	cpdfexamples.makefile
Source3:	afm2pfm.make
Patch0:		cpdfmakefile3.patch
Patch1:		cpdfconfig3.patch
Copyright:	Free for non-commercial use
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	zlib
Requires:	xpdf
Requires:	ghostscript-fonts

%description
This is a library of ANSI C functions, for creating PDF files directly
via C.

%package devel
Summary:	Header files needed for gd development
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Requires:	zlib-devel

%description devel
This package includes the header files for developing programs using
clibpdf.

%package static
Summary:	Static libraries needed for gd development
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}
Requires:	zlib-devel

%description static
This package includes static libraries needed for developing
programs using clibpdf.

%prep
%setup -q -n ClibPDF
%patch0
%patch1

%build
cp $RPM_SOURCE_DIR/cpdfexamples.makefile examples/Makefile
cd sourceP
export CFLAGS="%{rpmcflags} -DLinux -fPIC"
export VERSION="%{version}"
%{__make} -f Makefile.Linux shlib
export CFLAGS="%{rpmcflags} -DLinux"
cd ../util/t1utils-1.9
./configure --prefix=$RPM_BUILD_ROOT%{_prefix}
%{__make} install
cd ../afm2pfm
cp $RPM_SOURCE_DIR/afm2pfm.make .
%{__make} -f afm2pfm.make
install -m 755 afm2pfm pfm2afm $RPM_BUILD_ROOT%{_bindir}
install -m 644 README.afmpfm $RPM_BUILD_ROOT/doc


%install
rm -rf $RPM_BUILD_ROOT
cd sourceP
install -d $RPM_BUILD_ROOT%{_prefix}/{lib,include,bin,man/man1}
install cpdflib.h $RPM_BUILD_ROOT%{_includedir}
install -m 755 %{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}
install %{name}.a $RPM_BUILD_ROOT%{_libdir}
ln -sf %{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}.so.%{minorversion}
ln -sf %{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}.so
install -d $RPM_BUILD_ROOT%{_datadir}/ghostscript/fonts/
cp *.pfm $RPM_BUILD_ROOT%{_datadir}/ghostscript/fonts
cp *.pfb $RPM_BUILD_ROOT%{_datadir}/ghostscript/fonts
cp fontmap.lst $RPM_BUILD_ROOT%{_datadir}/ghostscript/fonts


%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc sourceP/README* doc/*
%attr(755,root,root) %{_bindir}/*
%{_prefix}/man/*
%{_datadir}/ghostscript/fonts/*.pfm
%{_datadir}/ghostscript/fonts/*.pfb
%{_datadir}/ghostscript/fonts/fontmap.lst
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}.so

%files devel
%defattr(644,root,root,755)
%doc examples/ 
%defattr(-,root,root)
%{_includedir}/cpdflib.h

%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a
