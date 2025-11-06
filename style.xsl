<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" omit-xml-declaration="yes" version="1.0" encoding="utf-8" indent="yes"/>

<xsl:template match="/ROWSET">
    <table border="1">
        <xsl:for-each select="ROW">
            <tr>
                <xsl:apply-templates select="@*[starts-with(name(), 'col')]"/>
            </tr>
        </xsl:for-each>
    </table>
</xsl:template> 

<xsl:template match="@*[../@ITEM='Label']">
    <th>
        <xsl:value-of select="."/>
    </th>
</xsl:template> 

<xsl:template match="@*">
    <td>
        <xsl:value-of select="."/>
    </td>
</xsl:template> 

</xsl:stylesheet>