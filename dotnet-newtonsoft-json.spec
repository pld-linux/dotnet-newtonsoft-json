%include	/usr/lib/rpm/macros.mono
Summary:	Json.NET - a popular high-performance JSON framework for .NET
Summary(pl.UTF-8):	Json.NET - popularny, wydajny szkielet JSON dla .NET
Name:		dotnet-newtonsoft-json
Version:	9.0.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/JamesNK/Newtonsoft.Json/releases
Source0:	https://github.com/JamesNK/Newtonsoft.Json/archive/%{version}/Newtonsoft.Json-%{version}.tar.gz
# Source0-md5:	737f366d719f7eb761c585ab755ade2e
Source1:	newtonsoft-json.pc.in
Source2:	Newtonsoft.Json.source
URL:		http://james.newtonking.com/json
BuildRequires:	mono-csharp
# xbuild
BuildRequires:	mono-devel
BuildRequires:	mono-monodoc
BuildRequires:	rpmbuild(macros) >= 1.446
BuildRequires:	rpmbuild(monoautodeps)
Requires:	mono
ExclusiveArch:	%{ix86} %{x8664} arm ia64 ppc s390 s390x sparc sparcv9 sparc64
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Json.NET is a popular high-performance JSON framework for .NET.
Features:
- Flexible JSON serializer for converting between .NET objects and
  JSON
- LINQ to JSON for manually reading and writing JSON
- High performance, faster than .NET's built-in JSON serializers
- Write indented, easy to read JSON
- Convert JSON to and from XML
- Supports .NET 2, .NET 3.5, .NET 4, Silverlight, Windows Phone and
  Windows 8.

%description -l pl.UTF-8
Json.NET to popularny, wydajny szkielet JSON dla .NET. Cechują go:
- elastyczna serializacja JSON do konwersji między obiektami .NET i
  JSON
- LINQ do JSON do ręcznego odczytu i zapisu formatu JSON
- wydajna, szybsza niż wbudowana w .NET serializacja JSON
- zapis czytelnego, zawierającego wcięcia formatu JSON
- konwersja JSON do i z XML
- obsługa .NET 2, .NET 3.5, .NET 4, Silverlight, Windows Phone oraz
  Windows 8.

%package devel
Summary:	Development files for Json.NET library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Json.NET
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for Json.NET library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki Json.NET.

%prep
%setup -q -n Newtonsoft.Json-%{version}

%build
# rules taken from Debian packaging
xbuild Src/Newtonsoft.Json/Newtonsoft.Json.Net40.csproj \
	/property:SignAssembly=true \
	/property:AssemblyOriginatorKeyFile=Dynamic.snk \
	/property:Configuration=Release \
	/property:DefineConstants='SIGNED NET40 TRACE'
mdoc update \
	-o monodoc \
	-i Src/Newtonsoft.Json/bin/Release/Net40/Newtonsoft.Json.xml \
	Src/Newtonsoft.Json/bin/Release/Net40/Newtonsoft.Json.dll
mdoc assemble \
	--format ecma \
	--out Newtonsoft.Json \
	monodoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_npkgconfigdir},%{_prefix}/lib/monodoc/sources}

gacutil -f -i Src/Newtonsoft.Json/bin/Release/Net40/Newtonsoft.Json.dll \
	/package Newtonsoft.Json-9.0 \
	/gacdir $RPM_BUILD_ROOT%{_prefix}/lib

cp -p Newtonsoft.Json.{zip,tree} %{SOURCE2} $RPM_BUILD_ROOT%{_prefix}/lib/monodoc/sources

%{__sed} -e 's,@prefix@,%{_prefix},' \
	-e 's,@VERSION@,%{version},' \
	-e 's,@MAJOR@,9.0,' \
	%{SOURCE1} > $RPM_BUILD_ROOT%{_npkgconfigdir}/newtonsoft-json.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md Doc/readme.txt
%{_prefix}/lib/mono/gac/Newtonsoft.Json

%files devel
%defattr(644,root,root,755)
%{_prefix}/lib/mono/Newtonsoft.Json-9.0
%{_prefix}/lib/monodoc/sources/Newtonsoft.Json.*
%{_npkgconfigdir}/newtonsoft-json.pc
