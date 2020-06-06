package shellcuts.core.structures

case class Configuration(
  crumb: Option[String],
  defaultFollow: Option[String],
  shellcuts: List[Shellcut]
)
