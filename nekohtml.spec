Summary:	HTML scanner and tag balancer
Summary(pl.UTF-8):	Narzędzie do skanowania i równoważenia znaczników HTML
Name:		nekohtml
Version:	0.9.5
Release:	1
License:	Apache-like
Group:		Applications/Text
Source0:	http://www.apache.org/~andyc/neko/%{name}-%{version}.tar.gz
# Source0-md5:	a5b22b189f23d0648eabc308fcfd4542
Source1:	%{name}-filter.sh
Patch0:		%{name}-crosslink.patch
Patch1:		%{name}-HTMLScanner.patch
URL:		http://www.apache.org/~andyc/neko/doc/html/
BuildRequires:	ant
BuildRequires:	java-gcj-compat-devel
BuildRequires:	xerces-j >= 2.3.0
Requires:	xerces-j >= 2.3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NekoHTML is a simple HTML scanner and tag balancer that enables
application programmers to parse HTML documents and access the
information using standard XML interfaces. The parser can scan HTML
files and "fix up" many common mistakes that human (and computer)
authors make in writing HTML documents. NekoHTML adds missing parent
elements; automatically closes elements with optional end tags; and
can handle mismatched inline element tags. NekoHTML is written using
the Xerces Native Interface (XNI) that is the foundation of the
Xerces2 implementation. This enables you to use the NekoHTML parser
with existing XNI tools without modification or rewriting code.

%description -l pl.UTF-8
NekoHTML to proste narzędzie do skanowania i równoważenia znaczników
HTML pozwalające programistom aplikacji na analizę dokumentów HTML i
dostęp do informacji przy użyciu standardowych interfejsów XML.
Analizator potrafi skanować pliki HTML i "poprawiać" wiele popularnych
błędów popełnianych przez autorów (ludzi i programy) piszących
dokumenty HTML. NekoHTML dodaje brakujące elementy rodzicielskie;
automatycznie zamyka elementy z opcjonalnymi znacznikami końcowymi;
potrafi obsłużyć niedopasowane znaczniki elementów inline. NekoHTML
jest napisane przy użyciu natywnego interfejsu Xercesa (XNI) będącego
podstawą implementacji Xerces2. Pozwala to używać analizatora NekoHTML
z istniejącymi narzędziami XNI bez modyfikowania czy przepisywania
kodu.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package demo
Summary:	Demo for %{name}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{name}
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -b .sav
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=$(build-classpath xerces-j2)
ant -f build-html.xml \
	-Dbuild.compiler=extJavac \
	-Djarfile=%{name}-%{version}.jar \
	-DjarfileXni=%{name}-xni-%{version}.jar \
	-DjarfileSamples=%{name}-samples-%{version}.jar \
	-Dj2se.javadoc=%{_javadocdir}/java \
	-Dxni.javadoc=%{_javadocdir}/xerces-j2-xni \
	-Dxerces.javadoc=%{_javadocdir}/xerces-j2-impl \
	clean package jar-xni test

%install
rm -rf $RPM_BUILD_ROOT

# Jars
install -d $RPM_BUILD_ROOT%{_javadir}
install -p %{name}{,-xni}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}-xni-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-xni.jar

# Scripts
install -Dpm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}-filter

# Samples
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install -p %{name}-samples-%{version}.jar \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# Javadocs
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a bin/package/nekohtml-*/doc/html/javadoc/* \
	$RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# Avoid having javadocs in %doc.
rm -rf bin/package/nekohtml-*/doc/html/javadoc

# Fix link between docs and javadoc.
cd bin/package/nekohtml-*/doc/html
ln -sf %{_javadocdir}/%{name}-%{version} javadoc

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE* README* TODO* bin/package/nekohtml-*/doc/*
%attr(755,root,root) %{_bindir}/%{name}-filter
%{_javadir}/%{name}*.jar

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
