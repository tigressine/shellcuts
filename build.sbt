scalaVersion := "2.11.12"
nativeLinkStubs := true
scalaSource in Compile := baseDirectory.value / "source"
scalaSource in Test := baseDirectory.value / "specs"
cleanFiles += baseDirectory.value / "pack"
libraryDependencies ++= Seq(
  "org.scalatest" % "scalatest_native0.3_2.11" % "3.2.0-SNAP10"
)

enablePlugins(ScalaNativePlugin)

lazy val programVersion = settingKey[String]("The program version.")
programVersion := "1.4"

lazy val supportedShells = settingKey[List[String]]("All supported shells.")
supportedShells := List("bash", "dash", "zsh", "ksh", "fish")

lazy val scrub = taskKey[Unit]("Cleans repo and removes additional junk.")
scrub := {
  import scala.sys.process._

  clean.value
  "rm -rf target/ project/project/ project/target/ dist/" !
}

lazy val prepack = taskKey[Unit]("Executes required tasks before packaging.")
prepack := Def.sequential(
  clean,
  Compile / nativeLink
).value

lazy val packDeb = taskKey[Unit]("Creates a Debian package.")
packDeb := {
  prepack.value

  import java.nio.charset.StandardCharsets
  import java.nio.file.{
    Files,
    Paths
  }
  import scala.sys.process._

  val packageName = s"shellcuts_${programVersion.value}-1"
  val installRoot = s"pack/${packageName}"

  // Create all required directories for the packaging process.
  val requiredDirs = List(
    "dist",
    s"${installRoot}/DEBIAN",
    s"${installRoot}/usr/bin",
    s"${installRoot}/etc/shellcuts/shells/fish",
    s"${installRoot}/etc/shellcuts/shells/posix",
    s"${installRoot}/usr/share/man/man1",
    s"${installRoot}/usr/share/doc"
  )
  requiredDirs foreach {
    (path) => Files.createDirectories(Paths.get(path))
  }

  // Copy files into the packaging directory tree.
  val copies = Map(
    s"target/scala-2.11/shellcuts-out" -> s"${installRoot}/usr/bin/sc-core",
    s"docs/shellcuts.1" -> s"${installRoot}/usr/share/man/man1/shellcuts.1",
    s"docs/CHANGES.txt" -> s"${installRoot}/usr/share/doc/CHANGES.txt",
    s"docs/README.rst" -> s"${installRoot}/usr/share/doc/README.rst",
    s"docs/LICENSE.txt" -> s"${installRoot}/usr/share/doc/LICENSE.txt",
    s"shells/fish/shellcuts.fish" -> s"${installRoot}/etc/shellcuts/shells/fish/shellcuts.fish",
    s"shells/posix/shellcuts.sh" -> s"${installRoot}/etc/shellcuts/shells/posix/shellcuts.sh"
  )
  copies foreach {
    case (source, destination) => {
      Files.copy(Paths.get(source), Paths.get(destination))
    }
  }

  // Create the required Debian control file for metadata.
  val controlContents = s"""
    |Package: shellcuts
    |Version: ${programVersion.value}-1
    |Section: base
    |Priority: optional
    |Architecture: amd64
    |Depends: libre2-dev
    |Maintainer: Tiger Sachse <tgsachse@gmail.com>
    |Description: Directory shortcuts for your shell
    |""".stripMargin.replaceFirst("\n", "")
  Files.write(
    Paths.get(s"${installRoot}/DEBIAN/control"),
    controlContents.getBytes(StandardCharsets.UTF_8)
  )

  // Build the deb package.
  s"dpkg-deb --build ${installRoot} dist/${packageName}.deb" !
}

lazy val pack = taskKey[Unit]("Packages this software.")
pack := Def.sequential(
  packDeb
).value

lazy val integrate = taskKey[Unit]("Executes the integration tests.")
integrate := {
  import scala.sys.process._

  val testSuites = List(
    "integ/shellcut-creation-tests.sh"
  )

  supportedShells.value foreach {
    (shell) => {
      val functionSource = shell match {
        case "bash" | "dash" | "zsh" | "ksh" => {
          "/etc/shellcuts/shells/posix/shellcuts.sh"
        }
        case "fish" => {
          "/etc/shellcuts/shells/fish/shellcuts.fish"
        }
      }
      testSuites foreach {
        (suite) => s"${suite} ${shell} ${functionSource}" !
      }
    }
  }
}
