# Classical empirical-Bayes limma primary analysis.
# Run from the archive 06_geo directory. Set LIMMA_OUT to avoid overwriting archived outputs.
library(limma)
INPUT <- 'limma_v2'
OUT <- Sys.getenv('LIMMA_OUT', 'limma_v2')
dir.create(OUT, recursive = TRUE, showWarnings = FALSE)

plain <- function(mat, group, tag) {
  group <- factor(group, levels = c('Ctrl', 'Treat'))
  fit <- lmFit(mat, model.matrix(~group))
  fit <- eBayes(fit)
  tt <- topTable(fit, coef = 2, number = Inf, adjust.method = 'BH', sort.by = 'P')
  tt$gene <- rownames(tt)
  write.csv(tt, file.path(OUT, paste0(tag, '_limma_plainEB.csv')), row.names = FALSE)
  cat(tag, 'plain eBayes: BH<0.05=', sum(tt$adj.P.Val < 0.05),
      ' top=', tt$gene[1], '\n', sep = '')
  return(tt)
}

g1 <- as.matrix(read.csv(file.path(INPUT, 'GSE121297_genelog2_matrix.csv'), row.names = 1))
t1 <- plain(g1, c(rep('Ctrl', 3), rep('Treat', 3)), 'GSE121297_RCaB_vs_Ctrl')
g2 <- as.matrix(read.csv(file.path(INPUT, 'GSE248215_normalized_log2.csv'), row.names = 1))
t2 <- plain(g2, c(rep('Treat', 3), rep('Ctrl', 2)), 'GSE248215_DR24h_vs_Ctrl')

show_genes <- function(mat, genes, tag) {
  for (g in genes) if (g %in% rownames(mat))
    cat(tag, g, ':', paste(round(mat[g, ], 2), collapse = ' | '), '\n')
}
show_genes(g1, c('SELE', 'LTB', 'VCAM1', 'ICAM1'), 'GSE121297')
show_genes(g2, c('CCL2', 'SERPINE1', 'HAVCR1'), 'GSE248215')

a <- read.csv(file.path(INPUT, 'GSE121297_RCaB_vs_Ctrl_limma.csv'))
cat('GSE121297: plain-sig=', sum(t1$adj.P.Val < 0.05),
    ' trendrobust-sig=', sum(a$adj.P.Val < 0.05),
    ' shared=', sum(t1$gene[t1$adj.P.Val < 0.05] %in% a$gene[a$adj.P.Val < 0.05]), '\n')
b <- read.csv(file.path(INPUT, 'GSE248215_DR24h_vs_Ctrl_limma.csv'))
cat('GSE248215: plain-sig=', sum(t2$adj.P.Val < 0.05),
    ' trendrobust-sig=', sum(b$adj.P.Val < 0.05),
    ' shared=', sum(t2$gene[t2$adj.P.Val < 0.05] %in% b$gene[b$adj.P.Val < 0.05]), '\n')
