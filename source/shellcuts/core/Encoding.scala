package shellcuts.core

import java.nio.charset.Charset

object Encoding {
  val SmallDelimiter = "\0"
  val BigDelimiter = "\0\0\0"
  val GlobalsPattern = """^([^\0]*)\0([^\0]*)""".r
  val ShellcutPattern = """\0\0\0([^\0]+)\0([^\0]*)((?:\0[^\0]+)+)""".r
  val PathPattern = """\0([^\0]+)""".r

  // Decode a configuration string into a Configuration object.
  def decode(encoded: String): Configuration = {
    val (crumb, defaultFollow) = GlobalsPattern.findFirstIn(encoded) map {
      case GlobalsPattern(crumb, defaultFollow) => {
        (Option(crumb), Option(defaultFollow))
      }
    } getOrElse((None, None))

    val shellcuts = ShellcutPattern.findAllIn(encoded).toList map {
      case ShellcutPattern(name, follow, paths) => {
        Shellcut(
          name,
          Option(follow),
          PathPattern.findAllIn(paths).toList map {
            case PathPattern(path) => path
          }
        )
      }
    }

    Configuration(crumb, defaultFollow, shellcuts)
  }

  // Encode a Configuration object into a configuration string.
  def encode(charset: Charset)(configuration: Configuration): String = {
    val head = configuration.crumb.getOrElse("") +
      SmallDelimiter +
      configuration.defaultFollow.getOrElse("")

    val body = configuration.shellcuts map {
      (shellcut) => {
        (shellcut.name :: shellcut.follow.getOrElse("") :: shellcut.paths)
          .mkString(SmallDelimiter)
      }
    } mkString(BigDelimiter)

    head + BigDelimiter + body
  }
}
